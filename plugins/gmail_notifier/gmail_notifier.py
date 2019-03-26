#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    gmail_notifier.py
Description:
    Watchdog SSH Login project plugin that send an email through SMTP protocol using gmail, to 
    notify SSH login detection.
Author:
    Jose Miguel Rios Rubio
Creation date:
    26/03/2019
Last modified date:
    26/03/2019
Version:
    0.0.1
'''

####################################################################################################

### Imported modules ###

from sys import argv
from smtplib import SMTP, SMTPException
import socket

####################################################################################################

### Constants ###

GMAIL_SMTP = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
GMAIL_ACCOUNT = "user1234@gmail.com"
GMAIL_PASWORD = "pass1234"

EMAIL_FROM = GMAIL_ACCOUNT
EMAIL_TO = ["user9876@domain.org"]
MSG_SUBJECT = "SSH Login Detection"

MSG_HEADER = f"From: From Watchdog SSH Login <{EMAIL_FROM}>\n" \
             f"To: To Person <{EMAIL_TO[0]}>\n" \
             f"Subject: {MSG_SUBJECT}"

MSG_BODY = "\nDetected a SSH Login in {}\n\nConnection:\n{}\n\n"

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
    # Prepare message content
    msg_content = MSG_BODY.format(system_ip, connection_from)
    message = f"{MSG_HEADER}\n{msg_content}"
    # Try to send the email
    try:
        smtp_client = SMTP(GMAIL_SMTP,587)
        smtp_client.starttls()
        smtp_client.login(GMAIL_ACCOUNT, GMAIL_PASWORD)
        smtp_client.sendmail(EMAIL_FROM, EMAIL_TO, message)         
        print("Email successfully sent.")
    except SMTPException as e:
        print(f"Error: Unable to send email. {e}")
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
