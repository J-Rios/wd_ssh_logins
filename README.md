# wd_ssh_logins
Linux tool that periodically monitorize and check for successfull SSH logins in the actual system, determine if a new login has occurred, and run the response subprograms (plugins) to act accordingly when a login has been detected.

Notes:
  - Tool developed for Python 3.6 or higher.
  - At the moment, the tool only support Debian/Ubuntu distributions (the ones that uses /var/log/auth.log file).
  - At the moment, the tool just detect SSH logins for systems configured in english language.
