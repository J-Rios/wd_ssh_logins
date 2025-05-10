#!/usr/bin/env bash

cat /var/log/auth.log | grep "sshd" | grep -e "Accepted password for " -e "Accepted publickey for " | awk '{print $1 " " $2 " " $7 " - " $9 ":" $11}'
exit 0
