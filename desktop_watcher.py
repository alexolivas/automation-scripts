import imghdr
import os
import shutil
import time

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


home_dir = str(Path.home())
desktop_dir = f"{home_dir}/DESKTOP"


class DesktopWatchHandler(FileSystemEventHandler):
    """
    Watches for file system events on the user's desktop and when anything is
    modified on there this handler sorts whatever is created into a specific
    folder on their documents directory to help keep the desktop clutter free.
    """

    def __init__(self):
        super(FileSystemEventHandler, self).__init__()

        # TODO: This could be made configurable at some point
        self.sort_rules = {
            "image": "Images",
            "misc": "Miscellaneous",
            "screen_shot": "Screenshots",
        }

        self.__create_sort_directories()

    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        :param event:
            Event representing file/directory modification.
        :type event:
            :class:`DirModifiedEvent` or :class:`FileModifiedEvent`
        """
        if desktop_dir == event.src_path:
            # Just an additional security check that ensures that the logic to sort
            # any new desktop files/directories only runs when a modification is made
            # on the user's desktop
            self.__sort_desktop_files()

    def __create_sort_directories(self):
        """
        This method is responsible for creating all the directories our
        script will be sorting any file created on the desktop
        """
        # TODO: we could make this configurable somehow, look into this for the next version
        # TODO: This should also be a key/value pair so that the rules and directories can be dynamic
        for sort_directory in self.sort_rules.values():
            # TODO Make the base directory configurable, don't create if it already exists
            new_dir = f"{home_dir}/Documents/{sort_directory}"
            Path(new_dir).mkdir(parents=True, exist_ok=True)

    def __sort_desktop_files(self):
        """
        This method is responsible for sorting any file or directory created on the
        desktop into a directory based on pre-configured rules
        """
        ignore_files = [".DS_Store", ".localized"]
        desktop_dir = f"{home_dir}/DESKTOP"
        documents_dir = f"{home_dir}/Documents"

        for filename in os.listdir(desktop_dir):
            if filename not in ignore_files:
                # The default destination location is the "miscellaneous" directory
                dest_dir = self.sort_rules["misc"]

                src_path = f"{desktop_dir}/{filename}"
                is_directory = os.path.isdir(src_path)

                if os.path.islink(src_path):
                    # Symlinks are to be ignored
                    continue
                elif filename.startswith("Screen Shot"):
                    dest_dir = self.sort_rules["screen_shot"]
                elif not is_directory:
                    # When this path is not a directory, check if it is a valid
                    # image and if so, send it to the "image" directory
                    image_file_type = imghdr.what(src_path)
                    if image_file_type is not None:
                        dest_dir = self.sort_rules["image"]

                # TODO: add logic to rename a file if it already exists

                # Actually move the file or directory
                dest_path = f"{documents_dir}/{dest_dir}/{filename}"
                shutil.move(src_path, dest_path)


if __name__ == "__main__":
    desktop_watch_handler = DesktopWatchHandler()
    observer = Observer()
    observer.schedule(desktop_watch_handler, desktop_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
