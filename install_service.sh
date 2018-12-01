#!/bin/bash

# Check Args
if [ -z "$1" ] || [ $1 == "-h" ] || [ $1 == "--help" ]
    then
        echo "Usage: sudo install_service.sh /path/to/code"
	echo "       IMPORTANT - do not include a trailing slash"
        exit
fi

# Create the service file
echo "Creating Service File in /etc/systemd/system/ci-christmas-tree.service"
echo "
[Unit]
Description=CI Christmas Tree
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=$1
ExecStart=/bin/bash $1/run.sh

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ci-christmas-tree.service

# Enable the service
systemctl enable ci-christmas-tree

# Start the service
systemctl start ci-christmas-tree
echo "Please hold... Service Starting... (approx 35 sec wait time)"

# Delay here while the ci christmas tree starts (approx 35 sec)
sleep 35s
