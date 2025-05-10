#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    log2file_login.py
Description:
    Watchdog SSH Login project plugin that store in a file the detected
    login with system timestamp.
Author:
    Jose Miguel Rios Rubio
Date:
    10/05/2025
Version:
    1.1.0
'''

###############################################################################

### Imported modules ###
from sys import argv
from os import path, makedirs, environ
from datetime import datetime
from datetime import UTC as DATETIME_UTC
from time import strftime

###############################################################################

### Log File ###

#LOG_FILE = "/var/log/ssh_logins.log"  # This needs system privileges (sudo)
LOG_FILE = f"{environ['HOME']}/.ssh_logins.log"

###############################################################################

### Functions ###

def create_parents_dirs(file_path):
    '''
    Create all parents directories from provided file path
    (mkdir -p $file_path).
    '''
    try:
        parentdirpath = path.dirname(file_path)
        if not path.exists(parentdirpath):
            makedirs(parentdirpath, 0o775)
    except Exception as e:
        print(f"ERROR - Can't create parents directories of {file_path}. {e}")
        finish(1)


def file_write(file_path, text=""):
    '''Write text to provided file.'''
    create_parents_dirs(file_path)
    # Determine if file exists and set open mode to write or append
    if not path.exists(file_path):
        print(f"File {file_path} not found, creating it...")
    # Try to Open and write to file
    try:
        with open(file_path, 'a', encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"ERROR - Can't write to file {file_path}. {e}")
        finish(1)

###############################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    # Check if script is running with expected number of argument
    if len(argv) != 2:
        print("Error: This script needs 1 argument (login text).")
        finish(1)
    login = argv[1]
    # Create timestamp and store login in file
    actual_date = datetime.now(DATETIME_UTC).strftime("%Y-%m-%d %H:%M:%S")
    to_save_text = f"[{actual_date}] {login}\n"
    file_write(LOG_FILE, to_save_text)
    print(f"Login stored in {LOG_FILE}")
    finish(0)

###############################################################################

### Script End Functions ###

def finish(return_code):
    '''Finish function.'''
    print(f"\nPlugin stoped, exit({return_code}).\n")
    exit(return_code)

###############################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
