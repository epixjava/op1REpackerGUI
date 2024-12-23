import re
import subprocess
from subprocess import run
import platform
import string
import os

def get_windows_drives():
    from ctypes import windll
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives


def get_mount_from_line(line):
    match = re.match(r"^\s*(?P<device>/dev/\w+) on (?P<mount>[^\0]+) (type .*)?\(.*\)\s*$", line)
    
    if match:
        return (match.group("device"), match.group("mount"))
    return None

def is_poopy_mount(mount):
    
    if platform.system() == 'Windows':
        system_drive = os.environ.get('SystemDrive', 'C:')
        return mount.upper().startswith(system_drive.upper())
    else:
        BAD_PREFIX = ['/dev', '/sys', '/net', '/proc', '/run', '/boot']
        if mount in ["/", "/home"]: return True
        for prefix in BAD_PREFIX:
            if mount.startswith(prefix): return True
    return False

def get_potential_mounts():
    
    if platform.system() == 'Windows':
        drives = get_windows_drives()
        return [(drive, drive) for drive in drives if not is_poopy_mount(drive)]
    else:
        result = run(["mount"], stdout=subprocess.PIPE, universal_newlines=True)
        
        if result.returncode != 0:
            print("mount command appeared to fail")
            return None
        
        if result.stdout is None:
            print("uh oh")
            return None
        lines = result.stdout.split("\n")
        mounts = [get_mount_from_line(x) for x in lines]
        filtered = [x for x in mounts if x is not None and not is_poopy_mount(x[1])]
    return filtered