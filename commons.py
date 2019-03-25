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
    25/03/2019
Version:
    0.0.1
'''

####################################################################################################

### Imported modules ###
from os import popen, path, makedirs

####################################################################################################

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
