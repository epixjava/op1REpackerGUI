import os
import sys
import time
import opie
import click
import tarfile
import platform
from helpers import u, mount

# Constants for OP-1 USB identification
VENDOR_TE = 0x2367
PRODUCT_OP1 = 0x0002
OP1_BASE_DIRS = set(['tape', 'album', 'synth', 'drum'])

# Import Windows-specific modules only on Windows
if platform.system() == 'Windows':
    try:
        import win32api
        import win32file
    except ImportError:
        sys.exit("On Windows systems, this tool requires the pywin32 package. Please install it with: pip install pywin32 in terminal")

def get_removable_drives():
    
    if platform.system() != 'Windows':
        return []
        
    drives = []
    for letter in range(ord('A'), ord('Z')+1):
        drive = chr(letter) + ':\\'
        try:
            drive_type = win32file.GetDriveType(drive)
            if drive_type == win32file.DRIVE_REMOVABLE:
                drives.append(drive)
        except Exception as e:
            continue
    return drives

def is_connected():
    
    if platform.system() == 'Windows':
        return any(is_op1_drive(drive) for drive in get_removable_drives())
    else:
        try:
            import usb.core
            dev = usb.core.find(idVendor=VENDOR_TE, idProduct=PRODUCT_OP1)
            return dev is not None
        except ImportError:
            sys.exit("On Unix-like systems, this tool requires pyusb. Please install it with: pip install pyusb")

def is_op1_drive(path):
    
    try:
        path = os.path.normpath(path)
        subdirs = set(u.get_visible_folders(path))
        return OP1_BASE_DIRS.issubset(subdirs)
    except (PermissionError, FileNotFoundError):
        return False
    except Exception as e:
        print(f"Warning: Unexpected error checking path {path}: {str(e)}")
        return False

def wait_for_connection():
    
    try:
        print("Waiting for OP-1 to connect in disk mode (Shift+COM -> 3)...")
        while True:
            if is_connected():
                print("OP-1 connected and mounted!")
                return True
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)

def is_valid_mount(mount_point):
    
    try:
        mount_point = os.path.normpath(mount_point)
        return os.path.exists(mount_point) and is_op1_drive(mount_point)
    except Exception:
        return False

def get_mount_or_die_trying():
    
    if not is_connected():
        wait_for_connection()
    
    mount_point = find_op1_mount()
    if mount_point is None:
        print("Waiting for OP-1 disk to mount...")
        mount_point = wait_for_op1_mount()
        if mount_point is None:
            sys.exit("Failed to find mount point of OP-1. Make sure it's in DISK mode and mounted.")
    return os.path.normpath(mount_point)

def find_op1_mount():
    
    if platform.system() == 'Windows':
        for drive in get_removable_drives():
            if is_op1_drive(drive):
                print(f"Found OP-1 at {drive}")
                return drive
    else:
        mounts = mount.get_potential_mounts()
        if mounts:
            for device, mount_point in mounts:
                try:
                    if is_op1_drive(mount_point):
                        print(f"Found OP-1 at {mount_point}")
                        return mount_point
                except (PermissionError, FileNotFoundError):
                    continue
    return None

def wait_for_op1_mount(timeout=15):
    
    try:
        for i in range(timeout):
            print(f"Checking for OP-1 mount ({i+1}/{timeout})...")
            mount_point = find_op1_mount()
            if mount_point is not None:
                return mount_point
            time.sleep(1)
        print("Timed out waiting for mount.")
        return None
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)