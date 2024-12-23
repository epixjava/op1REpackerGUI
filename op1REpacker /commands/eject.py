import click
import subprocess
from subprocess import run
from helpers import op1

description = "  Eject your OP-1"

@click.command()
@click.argument('name', required=False)
def cli(name=None):
    
    if not op1.is_connected():
        exit("OP-1 doesn't appear to be connected.")
    mount = op1.find_op1_mount()
    if mount is None:
        exit("Looks like your best friend already dismounted.")

    click.echo("attempting to eject...")
    click.echo(run(["diskutil", "eject", mount], stderr=subprocess.STDOUT).stdout)
