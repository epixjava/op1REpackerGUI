import click
import usb.util
from helpers import op1, backups

description = " Performs a full backup of your device"

@click.command()
def cli():
    backups.assert_environment()

    mount = op1.get_mount_or_die_trying()
    print("Found at %s" % mount)

    archive_path = backups.generate_archive(mount, backups.BACKUPS_DIR)
    
    print(f"\nBackup completed successfully. Archive saved at: {archive_path}")
    input("Press Enter to return to OP-1 REpacker.")

if __name__ == "__main__":
    cli()