#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    watchdog_ssh_login.py
Description:
    Script that periodically check for successfull SSH logins in the actual system, determine if a 
    new login has occurred, and run the response subprograms (plugins) to act accordingly when a 
    login has been detected.
    Examples of response plugins subprograms:
      - Plugin that notify the detected SSH login to system owner via email, Telegram, Slack, 
      web service, webhook, etc.
      - Plugin to execute or make a custom action in the system.
      - Plugin to setup an specified system configuration to that loged user.
      - Whatever that crosses your mind...
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

from os import path, geteuid
from sys import exit
from time import sleep
from signal import signal, SIGTERM, SIGINT

from commons import *

####################################################################################################

MAIN_SCRIPT_PATH = path.dirname(path.realpath(__file__))

####################################################################################################

### Plugins to use ###

PLUGINS = [
    f"{MAIN_SCRIPT_PATH}/plugins/gmail_notifier/gmail_notifier.py"
]

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    # Check if it is running with root privileges
    #if geteuid() != 0:
        #print("You must run this tool with root privileges.\n")
        #finish(1)
    print("Script started.")
    # Load actual SSH logins
    ssh_logins = system_call("./ssh_check_logins.sh")
    l_last_logins = ssh_logins.split("\n")
    if len(l_last_logins) > 0:
        print("Previous logins:")
        for login in l_last_logins:
            print(f"  {login}")
        print(" ")
    while True:
        try:
            # Check if there is a new SSH login
            new_logins = []
            ssh_logins = system_call(f"{MAIN_SCRIPT_PATH}/ssh_check_logins.sh")
            l_logins = ssh_logins.split("\n")
            for login in l_logins:
                if login not in l_last_logins:
                    new_logins.append(login)
            l_last_logins = l_logins
            # Launch plugins if any login was detected
            for login in new_logins:
                print(f"New login: {login}")
                for plugin in PLUGINS:
                    print(system_call(f"python3 {plugin} \"{login}\""))
            # Wait 5s between checks
            sleep(5)
        except Exception as e:
            print(f"{e}")
            finish(1)
    finish(0)

####################################################################################################

### Script End Functions ###

def finish(return_code):
    '''Finish function.'''
    print(f"\nScript stoped, exit({return_code}).\n")
    exit(return_code)


def signal_handler(signal, frame):
    '''Termination signals (SIGINT, SIGTERM) handler for program process.'''
    finish(0)

# Signals attachment
signal(SIGTERM, signal_handler) # SIGTERM (kill pid) to signal_handler
signal(SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler

####################################################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
