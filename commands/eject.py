import os
import sys
import opie
import click
import shutil
import platform
import subprocess
from subprocess import run, PIPE, STDOUT, CalledProcessError
from helpers import u, op1

description = "  Eject your OP-1"

def eject_windows(mount_point):
    
    try:
        drive_letter = os.path.splitdrive(mount_point)[0]
        
        powershell_command = [
            "powershell",
            "-Command",
            f"""
            $driveEject = New-Object -comObject Shell.Application
            $driveEject.Namespace(17).ParseName(\"{drive_letter}\").InvokeVerb(\"Eject\")
            """
        ]
        
        result = run(powershell_command, stdout=PIPE, stderr=STDOUT, text=True)
        
        if result.returncode == 0:
            return "OP-1 safely ejected. Return to op1REpackerGUI"
        else:
            return f"Error ejecting OP-1: {result.stdout}"
        
            
    except Exception as e:
        return f"Failed to eject OP-1: {str(e)}"

def eject_unix(mount_point):
    
    try:
        if platform.system() == 'Darwin':  
            result = run(["diskutil", "eject", mount_point], 
                        stdout=PIPE, stderr=STDOUT, text=True)
            return result.stdout
        else:  
            unmount_result = run(["udisksctl", "unmount", "--block-device", mount_point],
                               stdout=PIPE, stderr=STDOUT, text=True)
            if unmount_result.returncode != 0:
                return f"Error unmounting OP-1: {unmount_result.stdout}"
            
            poweroff_result = run(["udisksctl", "power-off", "--block-device", mount_point],
                                stdout=PIPE, stderr=STDOUT, text=True)
            return poweroff_result.stdout
            
    except FileNotFoundError:
        return ("Error: Required system utilities not found.\n"
                "Please install: \n"
                "- macOS: diskutil (should be pre-installed)\n"
                "- Linux: udisks2 (sudo apt install udisks2 or equivalent)")
    except Exception as e:
        return f"Failed to eject OP-1: {str(e)}"

@click.command()
@click.argument('name', required=False)
def cli(name=None):
    
    if not op1.is_connected():
        click.echo("OP-1 doesn't appear to be connected.")
        sys.exit(1)
    
    mount = op1.find_op1_mount()
    if mount is None:
        click.echo("Looks like your OP-1 is already dismounted.")
        sys.exit(0)
    
    click.echo("Attempting to eject OP-1...")
    
    if platform.system() == 'Windows':
        result = eject_windows(mount)
    else:
        result = eject_unix(mount)
    
    click.echo(result)