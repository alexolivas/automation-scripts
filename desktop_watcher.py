"""
#!/usr/bin/env python
Requirements:
1) Should watch for file changes in the desktop in the background at all times
2) It should move files into the user's directory in the following way:
    - if screenshot move it into ~/Documents/Screenshots
    - else move into ~/Documents/<file-type> e.g word doc is moved to ~/Documents/word, png, gif, etc into ~/Documents/Pictures
3) Stretch Goal: remove screenshots that have not been renamed after X number of days (from the new screenshots directory)
4) Stretch Goal: should be robust enough to work in any OS (for now just make it work on a mac)
"""
import imghdr
import os
import shutil

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


home_dir = str(Path.home())
documents_dir = f"{home_dir}/Documents"
print(f"Home directory: {home_dir}")
print(f"Documents directory: {documents_dir}")

sort_rules = {
    "image": "Images",
    "misc": "Miscellaneous",
    "screen_shot": "Screenshots",
}

def create_sort_directories():
    """
    This method is responsible for creating all the directories our
    script will be sorting any file created on the desktop
    """
    # TODO: we could make this configurable somehow, look into this for the next version
    # TODO: This should also be a key/value pair so that the rules and directories can be dynamic
    for sort_directory in sort_rules.values():
        # TODO Make the base directory configurable
        new_dir = f"{home_dir}/Documents/{sort_directory}"
        Path(new_dir).mkdir(parents=True, exist_ok=True)

def sort_desktop_files():
    """
    This method is responsible for sorting any file created on the
    desktop into a directory based on pre-configured rules
    """
    ignore_files = [".DS_Store", ".localized"]
    desktop_dir = f"{home_dir}/DESKTOP"

    for filename in os.listdir(desktop_dir):
        if filename not in ignore_files:
            # The default destination location is the "miscellaneous" directory
            dest_dir = sort_rules["misc"]

            src_path = f"{desktop_dir}/{filename}"
            is_directory = os.path.isdir(src_path)

            if os.path.islink(src_path):
                # Symlinks are to be ignored
                continue
            elif filename.startswith("Screen Shot"):
                dest_dir = sort_rules["screen_shot"]
            elif not is_directory:
                # When this path is not a directory, check if it is a valid
                # image and if so, send it to the "image" directory
                image_file_type = imghdr.what(src_path)
                if image_file_type is not None:
                    dest_dir = sort_rules["image"]

            # TODO: add logic to rename a file if it already exists

            # Actually move the file or directory
            dest_path = f"{documents_dir}/{dest_dir}/{filename}"
            shutil.move(src_path, dest_path)


# class DesktopWatcher(FileSystemEventHandler):
#     pass


create_sort_directories()
sort_desktop_files()
