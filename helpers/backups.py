import os
import tarfile
from datetime import datetime
from tqdm import tqdm
from helpers import op1

BACKUPS_DIR = os.path.expanduser("~/opie/backups")

def assert_environment():
    if not os.path.exists(BACKUPS_DIR):
        os.makedirs(BACKUPS_DIR)

def generate_archive(mount=None, backups_dir=BACKUPS_DIR):
    if mount is None:
        mount = op1.get_mount_or_die_trying()

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    archive_name = f"opie-backup-{timestamp}.tar.xz"
    archive_path = os.path.join(backups_dir, archive_name)
    
    print(f"Writing backup as {archive_path}")
    
    total_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(mount)])
    
    with tarfile.open(archive_path, "w:xz") as tar:
        with tqdm(total=total_items, unit="item", desc="Backing up") as pbar:
            for child in os.listdir(mount):
                if not child.startswith('.'):
                    child_path = os.path.join(mount, child)
                    tar.add(child_path, child, recursive=False)
                    pbar.update(1)
                    if os.path.isdir(child_path):
                        for root, dirs, files in os.walk(child_path):
                            for name in files + dirs:
                                if not name.startswith('.'):
                                    full_path = os.path.join(root, name)
                                    archive_name = os.path.relpath(full_path, mount)
                                    tar.add(full_path, archive_name)
                                    pbar.update(1)
    
    return archive_path

def restore_archive(archive_path, mount=None, progress_callback=None):
    if mount is None:
        mount = op1.get_mount_or_die_trying()

    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Backup file not found: {archive_path}")

    if not os.path.ismount(mount):
        raise ValueError(f"Invalid mount point: {mount}")

    with tarfile.open(archive_path, "r:xz") as tar:
        members = tar.getmembers()
        total_members = len(members)

        for i, member in enumerate(members):
            tar.extract(member, path=mount)
            if progress_callback:
                progress_callback(int((i + 1) / total_members * 100))

    print("Restore completed successfully.")