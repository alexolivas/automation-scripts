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


# class DesktopWatcher(FileSystemEventHandler):
#     pass

home_dir = str(Path.home())
print(f"Home directory: {home_dir}")
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

# from shutil import copyfile
# src = "/Users/OOLIVA282/Desktop/labreport.pdf"
# dst = "/Users/OOLIVA282/Desktop/TEST_FILE_COPY/copy.pdf"
# copyfile(src, dst)

# https://unix.stackexchange.com/questions/209646/how-to-activate-virtualenv-when-a-python-script-starts