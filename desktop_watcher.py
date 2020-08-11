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

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


home_dir = str(Path.home())
print(f"Home directory: {home_dir}")

def create_sort_directories():
    """
    This method is responsible for creating all the directories our
    script will be sorting any file created on the desktop
    """
    # TODO: we could make this configurable somehow, look into this for the next version
    sort_directories = [
        "Images",
        "Screenshots",
        "Miscellaneous",
    ]
    for sort_directory in sort_directories:
        # TODO Make the base directory configurable
        new_dir = f"{home_dir}/Documents/{sort_directory}"
        Path(new_dir).mkdir(parents=True, exist_ok=True)

def sort_desktop_files():
    """
    This method is responsible for sorting any file created on the
    desktop into a directory based on pre-configured rules
    """
    desktop_dir = f"{home_dir}/DESKTOP"
    num_screenshots = 0
    num_png = 0
    num_pdf = 0
    num_directories = 0
    num_unknown = 0
    for filename in os.listdir(desktop_dir):
        if filename.startswith("Screen Shot"):
            num_screenshots += 1
        elif filename.endswith(".pdf"):
            num_pdf += 1
        elif os.path.isdir(f"{desktop_dir}/{filename}"):
            num_directories += 1
        else:
            image_file_type = imghdr.what(f"{desktop_dir}/{filename}")
            if image_file_type is not None:
                num_png += 1
            else:
                num_unknown += 1
        # print(filename)

    print(f"Num screenshots: {str(num_screenshots)}")
    print(f"Num pdf: {str(num_pdf)}")
    print(f"Num images: {str(num_png)}")
    print(f"Num directories: {str(num_directories)}")
    print(f"Num unknown: {str(num_unknown)}")

# class DesktopWatcher(FileSystemEventHandler):
#     pass

create_sort_directories()
sort_desktop_files()
