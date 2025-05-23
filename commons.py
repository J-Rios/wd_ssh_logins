#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    commons.py
Description:
    Commons auxiliars functions for main project.
Author:
    Jose Miguel Rios Rubio
Creation date:
    25/03/2019
Last modified date:
    28/03/2019
Version:
    0.0.1
'''

####################################################################################################

### Imported modules ###
from os import popen, path, makedirs
from sys import version_info
from datetime import datetime
from datetime import UTC as DATETIME_UTC

####################################################################################################

def printts(text="", timestamp=True):
    '''Print with timestamp.'''
    # Normal print if timestamp is disabled or no text provided
    if not timestamp or text == "":
        print(text)
    else:
        # Normal print for all text start EOLs
        num_eol = -1
        for character in text:
            if character == '\n':
                print()
                num_eol = num_eol + 1
            else:
                break
        # Remove all text start EOLs (if any)
        if num_eol != -1:
            text = text [num_eol+1:]
        # Get actual time and print text with timestamp
        actual_date = datetime.now(DATETIME_UTC).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{actual_date}: {text}")


def is_running_with_py2():
    '''Check if script is running using Python 2.'''
    if version_info[0] == 2:
        return True
    return False


def is_running_with_py3():
    '''Check if script is running using Python 3.'''
    if version_info[0] == 3:
        return True
    return False


def system_call(command):
    '''Make a system call and return stdout response.'''
    response = ""
    try:
        f = popen(command)
        for line in f.readlines():
            response += line
        response = response[:-1]
    except Exception as e:
        print(f"{e}")
    return response


def create_parents_dirs(file_path):
    '''Create all parents directories from provided file path (mkdir -p $file_path).'''
    try:
        parentdirpath = path.dirname(file_path)
        if not path.exists(parentdirpath):
            makedirs(parentdirpath, 0o775)
    except Exception as e:
        print(f"ERROR - Can't create parents directories of {file_path}. {e}")


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


def file_read_all_text(file_path):
    '''Read all text file content and return it in a string.'''
    read = ""
    # Check if file doesnt exists
    if not path.exists(file_path):
        print("ERROR - File {} not found.".format(file_path))
    # File exists, so open and read it
    else:
        try:
            if is_running_with_py3():
                with open(file_path, "r", encoding="utf-8") as f:
                    read = f.read()
            else:
                with open(file_path, "r") as f:
                    read = f.read()
        except Exception as e:
            print("ERROR - Can't open and read file {}. {}".format(file_path, str(e)))
    return read
