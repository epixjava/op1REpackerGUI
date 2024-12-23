import os
import sys
import time
import opie
import click
import tarfile
from helpers import op1, rips

description = "    Rips album side A and B and saves as flac/mp3/m4a"

@click.command()
@click.option('--name', '-n', prompt='Enter a name for the rip', help='Name for the rip')
def cli(name=None):
    if name is None:
        name = click.prompt('Enter a name for the rip')
    rips.assert_environment()
    mount = op1.get_mount_or_die_trying()
    print(f"Found at {mount}")
    rips.create_rip(mount, name)

if __name__ == '__main__':
    cli()