import os
import sys
import time
import usb.core
import usb.util
import platform
from pathlib import Path

VENDOR_TE = 0x2367
PRODUCT_OP1 = 0x0002
OP1_BASE_DIRS = set(['tape', 'album', 'synth', 'drum'])

def get_system_type():
    """Determine the operating system."""
    system = platform.system().lower()
    return system

def ensure_connection():
    """Ensure OP-1 is connected in disk mode."""
    if not is_connected():
        print("Please connect your OP-1 and put it in DISK mode (Shift+COM -> 3)...")
        wait_for_connection()

def is_connected():
    """Check if OP-1 is connected via USB."""
    return usb.core.find(idVendor=VENDOR_TE, idProduct=PRODUCT_OP1) is not None

def wait_for_connection():
    """Wait for OP-1 to connect."""
    try:
        while True:
            time.sleep(1)
            if is_connected():
                break
    except KeyboardInterrupt:
        sys.exit(0)

def get_windows_mount_points():
    """Get potential mount points on Windows."""
    from string import ascii_uppercase
    return [f"{d}:\\" for d in ascii_uppercase if os.path.exists(f"{d}:\\")]

def get_macos_mount_points():
    """Get potential mount points on macOS."""
    volumes_path = Path("/Volumes")
    if volumes_path.exists():
        return [str(p) for p in volumes_path.iterdir() if p.is_dir()]
    return []

def get_linux_mount_points():
    """Get potential mount points on Linux."""
    media_paths = [Path("/media"), Path("/mnt")]
    mount_points = []
    for base_path in media_paths:
        if base_path.exists():
            # Include both /media and /media/username paths
            mount_points.extend([str(p) for p in base_path.iterdir() if p.is_dir()])
            if base_path.name == "media" and os.getenv("USER"):
                user_media = base_path / os.getenv("USER")
                if user_media.exists():
                    mount_points.extend([str(p) for p in user_media.iterdir() if p.is_dir()])
    return mount_points

def validate_op1_mount(path):
    """Validate if a path contains OP-1 directory structure."""
    try:
        subdirs = set(entry.name for entry in os.scandir(path) if entry.is_dir())
        return OP1_BASE_DIRS.issubset(subdirs)
    except (PermissionError, FileNotFoundError):
        return False

def find_op1_mount():
    """Find OP-1 mount point across different operating systems."""
    system = get_system_type()
    
    # Get potential mount points based on OS
    if system == "windows":
        mount_points = get_windows_mount_points()
    elif system == "darwin":
        mount_points = get_macos_mount_points()
    elif system == "linux":
        mount_points = get_linux_mount_points()
    else:
        print(f"Unsupported operating system: {system}")
        return None

    # Check each mount point for OP-1 directory structure
    for mount_point in mount_points:
        if validate_op1_mount(mount_point):
            return mount_point

    return None

def wait_for_op1_mount(timeout=5):
    """Wait for OP-1 to mount with timeout."""
    i = 0
    try:
        while i < timeout:
            time.sleep(1)
            mount_point = find_op1_mount()
            if mount_point is not None:
                return mount_point
            i += 1
        print("Timed out waiting for mount.")
        return None
    except KeyboardInterrupt:
        sys.exit(0)

def get_mount_or_die_trying():
    """Main function to get OP-1 mount point."""
    ensure_connection()
    mount_point = find_op1_mount()
    if mount_point is None:
        print("Waiting for OP-1 disk to mount...")
        mount_point = wait_for_op1_mount()
        if mount_point is None:
            sys.exit("Failed to find mount point of OP-1. Please ensure it's properly connected in DISK mode.")
    return mount_point