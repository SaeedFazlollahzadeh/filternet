# Description

This script, based on being on Windows or Linux, detects your default gateway IP and your default ethernet device and runs `nslookup` for the list of domains you provice in the list.

Then creates the required command based on your OS, and automatically runs the file to add them to routing table.

If needed, comment line 22 (Linux) or 47 (Windows) to prevent running the script, and only generating the file.
