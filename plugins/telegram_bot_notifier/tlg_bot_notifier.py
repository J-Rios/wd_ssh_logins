#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    tlg_bot_notifier.py
Description:
    Watchdog SSH Login project plugin that send a telegram message to
    specified chat through a telegram Bot to notify SSH login detection.
Author:
    Jose Miguel Rios Rubio
Date:
    10/05/2025
Version:
    1.1.0
'''

###############################################################################

### Imported modules ###

import socket
import sys
import urllib.parse
import urllib.request

###############################################################################

### Constants ###

BOT_TOKEN = "XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TO_CHAT_ID = 000000000

MSG_TEXT = \
    "SSH Login\n" \
    "——————————\n" \
    "\n" \
    "System:\n" \
    "    {} ({}) \n" \
    "\n" \
    "User:\n" \
    "    {}\n" \
    "\n" \
    "From:\n" \
    "    {}\n" \
    "\n" \
    "Date:\n" \
    "    {}\n"

TLG_BOT_API_URL = "https://api.telegram.org"
TLG_BOT_API = f"{TLG_BOT_API_URL}/bot{BOT_TOKEN}"
TLG_BOT_API_SEND_MSG = f"{TLG_BOT_API}/sendMessage"

###############################################################################

### Auxiliary Functions ###

def get_system_ip_address():
    '''Get current system local IP address.'''
    ip_addr = "127.0.0.1"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

def tlg_send_msg(chat_id, msg_text):
    '''Send a Telegram message.'''
    params = {
        "chat_id": str(chat_id),
        "text": msg_text,
        "parse_mode": "HTML"
    }
    try:
        url = TLG_BOT_API_SEND_MSG + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url) as response:
            response = response.read().decode("utf-8")
            return True
    except Exception as e:
        print(f"Fail to send Telegram Message: {e}")
        return False

###############################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    # Check if script is running with expected number of argument
    if len(sys.argv) != 2:
        print("Error: This script needs 1 argument (email message content).")
        finish(1)
    connection_data = sys.argv[1].split(" ")
    date = connection_data[0]
    system_host = connection_data[1]
    user = connection_data[2]
    connection_from = connection_data[4]
    # Get system IP address
    system_ip = get_system_ip_address()
    # Create message and try to send it
    msg = MSG_TEXT.format(system_host, system_ip, user, connection_from, date)
    if tlg_send_msg(TO_CHAT_ID, msg):
        print("Telegram message successfully sent.")
    else:
        print("Error: Unable to send message.")
        finish(1)
    finish(0)

###############################################################################

### Script End Functions ###

def finish(return_code):
    '''Finish function.'''
    print(f"\nPlugin stopped, exit({return_code}).\n")
    sys.exit(return_code)

###############################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
