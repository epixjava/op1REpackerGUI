import click
import os
import shutil
from helpers import op1

description = "Provides amount of OP-1 patches installed and reports storage usage."

@click.command()
def cli():
    mount_point = op1.get_mount_or_die_trying()
    
    synth_sampler_files = 0
    synth_synthesis_files = 0
    drum_files = 0
    
    for folder in ['synth', 'drum']:
        folder_path = os.path.join(mount_point, folder)
        for root, dirs, files in os.walk(folder_path):
            if 'user' in dirs:
                dirs.remove('user')  
            for file in files:
                if file.lower().endswith('.aif'):
                    if folder == 'synth':
                        if 'sampling' in root.lower():
                            synth_sampler_files += 1
                        else:
                            synth_synthesis_files += 1
                    else:  
                        drum_files += 1
    
    total, used, free = shutil.disk_usage(mount_point)
    used_percentage = (used / total) * 100
    
    click.echo("\nStorage Usage:")
    click.echo(f"Total: {total // (2**20):.1f} MB")
    click.echo(f"Used: {used // (2**20):.1f} MB ({used_percentage:.1f}% used)")
    click.echo(f"Free: {free // (2**20):.1f} MB")
    
    click.echo("\nPatch Usage:")
    click.echo(f"Synth Sampler patches: {synth_sampler_files} / 42 maximum")
    click.echo(f"Synth patches: {synth_synthesis_files} / 100 maximum")
    click.echo(f"Drum patches: {drum_files} / 42 maximum")
    
    click.echo("\nVisit op1.fun for custom patches,synths and drum kits!")
    click.echo("\nYour device is mounted and ready for file transfer.")

    click.pause("\nYour OP-1 will remain mounted until you eject it.\nPress any key to close...")

if __name__ == '__main__':
    cli()