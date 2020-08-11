# Automation Scripts

A collection of python scripts to help organize files and automate repetitive tasks

## Installation

Clone the repo anywhere on your computer

### Virtualenv

If you are using pyenv and pyenv-virtualenv you can create your virtual environment

```bash
pyenv virtualenv 3.8.2 <virtualenv-name>
```

Then activate it

```bash
pyenv activate <virtualenv-name>
```

### Dependencies

This project only depends on `watchdog` to watch for file changes. Run the following command to install this

```bash
pip install watchdog
```

### Automator

On a mac you can use the built-in automator to automate your these python scripts.

#### `bash desktop_watcher.py`

Open automator

Select Library > Utilities > "Run Shell Script"

Select "/bin/bash"

Type the following in the text area:

```bash
cd /<directory-to-local-repo>/automation-scripts/
/<python-location>/python desktop_watcher.py
```

NOTE: if you are using pyenv you can set the python version you want to run by running your script like this:

```bash
# You can get this location by activating your virtualenv and running "pyenv which python"
/Users/<username>/.pyenv/versions/<virtualenv-name>/bin/python desktop_watcher.py
```

Save the automation task

### Schedule

To run it on startup, go to System Preferences > Users and Groups > Login Items

Click on the plus sign and find the automation task you just created to add it to the list of items to run on startup

<!-- chmod +x <script-name> -->

<!-- https://janakiev.com/blog/python-background/ -->
