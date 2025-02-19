import os
import tarfile
from datetime import datetime
from tqdm import tqdm
from helpers import op1, u  # Import our updated u.py helper

def get_backups_dir():
    
    backups_dir = os.path.join(u.HOME, "backups")
    return backups_dir

BACKUPS_DIR = get_backups_dir()

def assert_environment():
    try:
        os.makedirs(BACKUPS_DIR, exist_ok=True)
    except Exception as e:
        raise EnvironmentError(f"Failed to create backups directory: {e}")

def generate_archive(mount=None, backups_dir=None):
    
    if mount is None:
        mount = op1.get_mount_or_die_trying()
    
    if backups_dir is None:
        backups_dir = BACKUPS_DIR

    os.makedirs(backups_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    archive_name = f"opie-backup-{timestamp}.tar.xz"
    archive_path = os.path.join(backups_dir, archive_name)
    
    print(f"Writing backup as {archive_path}")
    
    mount = os.path.normpath(mount)
    
    total_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(mount)])
    
    with tarfile.open(archive_path, "w:xz") as tar:
        with tqdm(total=total_items, unit="item", desc="Backing up") as pbar:
            for child in os.listdir(mount):
                if not child.startswith('.'):
                    child_path = os.path.join(mount, child)
                    archive_child = os.path.normpath(child)
                    tar.add(child_path, archive_child, recursive=False)
                    pbar.update(1)
                    
                    if os.path.isdir(child_path):
                        for root, dirs, files in os.walk(child_path):
                            for name in files + dirs:
                                if not name.startswith('.'):
                                    full_path = os.path.join(root, name)
                                    archive_name = os.path.normpath(
                                        os.path.relpath(full_path, mount)
                                    )
                                    tar.add(full_path, archive_name)
                                    pbar.update(1)
    
    return archive_path


def verify_backup_before_restore(backup_path):
    
    from commands import verify
    is_valid, issues = verify.verify_backup_structure(backup_path)
    return is_valid, issues

def restore_archive(archive_path, mount=None, progress_callback=None):
    
    if mount is None:
        mount = op1.get_mount_or_die_trying()

    archive_path = os.path.normpath(archive_path)
    mount = os.path.normpath(mount)

    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Backup file not found: {archive_path}")

    if not op1.is_valid_mount(mount):  
        raise ValueError(f"Invalid mount point: {mount}")

    try:
        with tarfile.open(archive_path, "r:xz") as tar:
            members = tar.getmembers()
            total_members = len(members)

            for i, member in enumerate(members):
                member.name = os.path.normpath(member.name)
                tar.extract(member, path=mount)
                if progress_callback:
                    progress_callback(int((i + 1) / total_members * 100))

        print("Restore completed successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to restore backup: {e}")