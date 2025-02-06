# verify.py
import click
import hashlib
import tarfile
from pathlib import Path
from helpers import backups
from datetime import datetime

description = " Verify the integrity of OP-1 backup files"

def calculate_file_hash(file_path):
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.digest()

def verify_backup_structure(archive_path):
    
    required_dirs = {'tape', 'album', 'synth', 'drum'}
    found_dirs = set()
    issues = []

    try:
        with tarfile.open(archive_path, 'r:xz') as tar:
            members = tar.getmembers()
            
            for member in members:
                top_level_dir = member.name.split('/')[0]
                found_dirs.add(top_level_dir)
            
            missing_dirs = required_dirs - found_dirs
            if missing_dirs:
                issues.append(f"Missing required directories: {', '.join(missing_dirs)}")
            
            for required_dir in required_dirs - missing_dirs:
                dir_contents = [m for m in members if m.name.startswith(required_dir)]
                if not dir_contents:
                    issues.append(f"Directory '{required_dir}' is empty")

    except Exception as e:
        issues.append(f"Error reading backup archive: {str(e)}")
        return False, issues

    return len(issues) == 0, issues

def store_backup_metadata(backup_path, metadata):

    metadata_path = backup_path.with_suffix('.meta')
    try:
        with open(metadata_path, 'w') as f:
            for key, value in metadata.items():
                f.write(f"{key}={value}\n")
    except Exception as e:
        click.echo(f"Warning: Could not save backup metadata: {str(e)}")

@click.command()
@click.argument('backup_file', required=False)
def cli(backup_file=None):

    try:
        backups.assert_environment()
        
        if not backup_file:
            backup_files = sorted(
                Path(backups.BACKUPS_DIR).glob("*.tar.xz"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            if not backup_files:
                click.echo("No backups found to verify.")
                return
            
            click.echo("Available backups:")
            for i, backup in enumerate(backup_files):
                size_mb = backup.stat().st_size / (1024 * 1024)
                click.echo(f"{i}. {backup.name} ({size_mb:.1f}MB)")
            
            choice = click.prompt("Choose a backup to verify", type=int)
            if choice < 0 or choice >= len(backup_files):
                click.echo("Invalid selection.")
                return
            
            backup_path = backup_files[choice]
        else:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                click.echo(f"Backup file not found: {backup_path}")
                return

        click.echo(f"\nVerifying backup: {backup_path.name}")
        
        click.echo("\nChecking backup structure...")
        is_valid, issues = verify_backup_structure(backup_path)
        
        if not is_valid:
            click.echo("\n Backup verification failed!")
            for issue in issues:
                click.echo(f" - {issue}")
            return

        click.echo("\nCalculating backup checksums...")
        backup_hash = calculate_file_hash(backup_path)
        
        metadata = {
            'last_verified': datetime.now().isoformat(),
            'size_bytes': backup_path.stat().st_size,
            'sha256': backup_hash.hex(),
            'structure_verified': 'true'
        }
        
        store_backup_metadata(backup_path, metadata)
        
        click.echo("\n  Backup verification successful!")
        click.echo(f"Backup size: {metadata['size_bytes'] / (1024*1024):.1f}MB")
        click.echo(f"SHA-256: {metadata['sha256']}")
        click.echo(f"Verified: {metadata['last_verified']}")
        click.pause("Press any key to return to op1-REpacker")

    except Exception as e:
        click.echo(f"\n  Error during verification: {str(e)}")
        return 1

if __name__ == '__main__':
    cli()