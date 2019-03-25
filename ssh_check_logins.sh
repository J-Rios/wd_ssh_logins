#!/usr/bin/env bash

cat /var/log/auth.log | grep "sshd" | grep "Accepted password for " | awk '{print $1 " " $2 " " $3 " - " $11 ":" $13}'

exit 0