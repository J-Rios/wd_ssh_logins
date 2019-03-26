# wd_ssh_logins
Linux tool that periodically monitorize and check for successfull SSH logins in the actual system, determine if a new login has occurred, and run the response subprograms (plugins) to act accordingly when a login has been detected.

Notes:
  - At the moment, the tool only support Debian/Ubuntu distributions (the ones that uses with /var/log/auth.log file).
  - At the moment, the tool only detect SSH logins for systems with english locales language configured system.
