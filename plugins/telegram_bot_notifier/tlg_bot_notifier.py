#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    tlg_bot_notifier.py
Description:
    Watchdog SSH Login project plugin that send a telegram message to specified chat through a 
    telegram Bot to notify SSH login detection.
Author:
    Jose Miguel Rios Rubio
Creation date:
    27/03/2019
Last modified date:
    27/03/2019
Version:
    0.0.1
'''

####################################################################################################

### Imported modules ###

from sys import argv
import socket
from telegram.ext import Updater
from telegram import ParseMode

####################################################################################################

### Constants ###

BOT_TOKEN = "XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TO_CHAT_ID = 000000000

MSG_BASE = "SSH Login Detected\n\nSystem:\n{}\n\nConnection from:\n<pre>{}</pre>"

####################################################################################################

### Auxiliar Functions ###

def get_system_ip_address():
    '''Get current system local IP address.'''
    ip_addr = "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    # Check if script is running with expected argument and get connection from
    if len(argv) != 2:
        print("Error: This script needs 1 argument (email message content).")
        finish(1)
    connection_from = argv[1]
    # Get system IP address
    system_ip = get_system_ip_address()
    # Create the Bot
    Bot = Updater(BOT_TOKEN).bot
    # Create message and try to send it
    msg = MSG_BASE.format(system_ip, connection_from)
    try:
        Bot.send_message(TO_CHAT_ID, msg, ParseMode.HTML)
        print("Telegram message successfully sent.")
    except Exception as e:
        print(f"Error: Unable to send message. {e}")
        finish(1)
    finish(0)

####################################################################################################

### Script End Functions ###

def finish(return_code):
    '''Finish function.'''
    print(f"\nPlugin stoped, exit({return_code}).\n")
    exit(return_code)

####################################################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
