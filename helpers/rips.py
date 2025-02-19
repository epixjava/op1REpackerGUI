import os
import sys
import time
import opie
import click
import shutil
import tarfile
import platform
from helpers import u
from datetime import datetime
from os import path
from subprocess import check_call, PIPE, STDOUT, CalledProcessError

# Define constants in a cross-platform way
RIPS_DIR = os.path.join(u.HOME, "rips")

def assert_environment():
    
    try:
        os.makedirs(RIPS_DIR, exist_ok=True)
    except Exception as e:
        raise EnvironmentError(f"Failed to create rips directory at {RIPS_DIR}: {e}")

def get_ffmpeg_binary():
    
    if platform.system() == 'Windows':
        common_paths = [
            os.path.join(os.getenv('ProgramFiles'), 'ffmpeg', 'bin', 'ffmpeg.exe'),
            os.path.join(os.getenv('ProgramFiles(x86)'), 'ffmpeg', 'bin', 'ffmpeg.exe'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'ffmpeg', 'bin', 'ffmpeg.exe')
        ]
        
        ffmpeg_path = shutil.which("ffmpeg.exe") or next((p for p in common_paths if os.path.exists(p)), None)
        if ffmpeg_path:
            return ffmpeg_path
            
    else:
        if shutil.which("ffmpeg"):
            return "ffmpeg"
        if shutil.which("avconv"):
            return "avconv"
    
    raise EnvironmentError(
        "Neither ffmpeg nor avconv found. Please install ffmpeg:\n"
        "- Windows: run 'winget install FFmpeg' in terminal\n"
        "- macOS: Use 'brew install ffmpeg'\n"
        "- Linux: Use your package manager (e.g., 'apt install ffmpeg')"
    )

def transcode(input_file, codec, output_file, codec_flags=None):
    
    if codec_flags is None:
        codec_flags = []

    try:
        binary = get_ffmpeg_binary()
        
        input_file = os.path.normpath(input_file)
        output_file = os.path.normpath(output_file)
        
        base_command = [
            binary,
            "-loglevel", "warning",
            "-stats",
            "-i", input_file,
            "-c:a", codec
        ]
        
        command = base_command + codec_flags + [output_file]
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        check_call(command, stderr=STDOUT)
        
    except CalledProcessError as e:
        raise RuntimeError(f"Transcoding failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error during transcoding: {str(e)}")

def create_rip(mount, name):
    
    try:
        fullpath = os.path.normpath(os.path.join(RIPS_DIR, name))
        albums = os.path.normpath(os.path.join(mount, "album"))
        sides = ["side_a", "side_b"]
        
        try:
            os.makedirs(fullpath)
        except FileExistsError:
            raise ValueError(f"Rip directory already exists: {fullpath}")
            
        click.echo(f"Writing rips to {fullpath}")
        
        for side in sides:
            input_file = os.path.join(albums, f"{side}.aif")
            
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Source file not found: {input_file}")
            
            click.echo(f"Transcoding {side}")
            flac_output = os.path.join(fullpath, f"{side}.flac")
            transcode(input_file, "flac", flac_output)
            
            click.echo("Creating additional formats...")
            
            click.echo(f"Transcoding {side} to ALAC")
            transcode(flac_output, "alac", os.path.join(fullpath, f"{side}.m4a"))
            
            click.echo(f"Transcoding {side} to MP3 V0")
            transcode(flac_output, "libmp3lame", 
                     os.path.join(fullpath, f"{side}.mp3"), 
                     ["-q:a", "0"])
        
        click.echo("\nRipping completed successfully!")
        click.pause("Press any key to return to op1-REpacker")
        
    except Exception as e:
        click.echo(f"Error during ripping process: {str(e)}", err=True)
        sys.exit(1)