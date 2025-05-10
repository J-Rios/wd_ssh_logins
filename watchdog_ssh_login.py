#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    watchdog_ssh_login.py
Description:
    Script that periodically check for successful SSH logins in the
    actual system, determine if a new login has occurred, and run the
    response subprograms (plugins) to act accordingly when a login has
    been detected.
    Examples of response plugins subprograms:
      - Plugin that notify the detected SSH login to system owner via
      email, Telegram, Slack, web service, webhook, etc.
      - Plugin to execute or make a custom action in the system.
      - Plugin to setup a specified system configuration for that
      logged user.
      - Whatever that crosses your mind...
Author:
    Jose Miguel Rios Rubio
Date:
    10/05/2025
Version:
    1.1.0
'''

###############################################################################

### Imported modules ###

import sys
from os import path
from time import sleep
from signal import signal, SIGTERM, SIGINT
from threading import Thread

from commons import printts, system_call, file_read_all_text

###############################################################################

MAIN_SCRIPT_PATH = path.dirname(path.realpath(__file__))
BASH_SCRIPT_CHECK_SSH_CONNECTION = f"{MAIN_SCRIPT_PATH}/ssh_check_logins.sh"

###############################################################################

### Plugins to use (comment/uncomment to disable/enable plugins) ###

PLUGINS = [
    f"{MAIN_SCRIPT_PATH}/plugins/log2file_login/log2file_login.py",
    f"{MAIN_SCRIPT_PATH}/plugins/gmail_notifier/gmail_notifier.py",
    f"{MAIN_SCRIPT_PATH}/plugins/telegram_bot_notifier/tlg_bot_notifier.py"
]

###############################################################################

### Withelist file ###

WHITELIST_F = f"{MAIN_SCRIPT_PATH}/whitelist.txt"

###############################################################################

### Threading Function that call plugins ###

def run_plugin(plugin, login):
    '''make a system call to execute the provided plugin.'''
    print(system_call(f"python3 {plugin} \"{login}\""))

###############################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    printts("Script started.")
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
            ssh_logins = system_call(BASH_SCRIPT_CHECK_SSH_CONNECTION)
            l_logins = ssh_logins.split("\n")
            for login in l_logins:
                if login not in l_last_logins:
                    new_logins.append(login)
            l_last_logins = l_logins
            # Launch plugins if any login was detected
            for login in new_logins:
                printts(f"New login detected: {login}")
                # Check and ignore if it is in the withelist
                withelist_text = file_read_all_text(WHITELIST_F)
                withelist_text = withelist_text.replace("\r,", "")
                withelist = withelist_text.split("\n")
                login_ip = login[login.find(" - ")+3:login.rfind(":")]
                if login_ip in withelist:
                    print(f"Ignoring known connection from {login_ip}")
                    continue
                for plugin in PLUGINS:
                    # Launch a new thread to handle plugin execution
                    th = Thread(target=run_plugin, args=(plugin, login))
                    th.start()
            # Wait 10s between checks
            sleep(10)
        except Exception as e:
            printts(f"{e}")
            finish(1)
    finish(0)

###############################################################################

### Script End Functions ###

def finish(return_code):
    '''Finish function.'''
    printts(f"\nScript stoped, exit({return_code}).\n")
    sys.exit(return_code)

def signal_handler(signal, frame):
    '''Termination signals (SIGINT, SIGTERM) handler.'''
    finish(0)

# Signals attachment
signal(SIGTERM, signal_handler) # SIGTERM (kill pid) to signal_handler
signal(SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler

###############################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
