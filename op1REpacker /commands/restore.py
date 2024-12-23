import os
import click
from helpers import u, op1, backups

description = "Choose a backup file and restore it to a plugged-in OP-1"

@click.command()
def cli():
    try:
        backups.assert_environment()

        click.echo(f"Backups found in {backups.BACKUPS_DIR}")
        archives = u.get_visible_children(backups.BACKUPS_DIR)
        if not archives:
            click.echo("No backups found. Please create a backup first.")
            return

        for i, archive in enumerate(archives):
            click.echo(f"{i}. {archive}")

        choice = click.prompt('Choose a backup', type=int)

        if choice < 0 or choice >= len(archives):
            click.echo("Invalid selection. Please try again.")
            return

        click.echo(f"You selected: {archives[choice]}")

        mount = op1.get_mount_or_die_trying()
        click.echo(f"OP-1 found at {mount}")

        backup_path = os.path.join(backups.BACKUPS_DIR, archives[choice])
        click.echo(f"Restoring {archives[choice]} to {mount}")
        
        with click.progressbar(length=100, label="Restoring backup") as bar:
            def update_progress(progress):
                bar.update(progress)
            backups.restore_archive(backup_path, mount, progress_callback=update_progress)

        click.echo("Restore completed successfully!")
        click.pause("\nPress any key to return to OP-1 REpacker")

    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")
        click.echo("Restore failed. Please try again with a fresh backup.")

if __name__ == "__main__":
    cli()
