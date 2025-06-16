#!/bin/bash
# This script is triggered by a udev rule when a block device is added.
# It waits a few seconds for the device to be mounted by the OS, 
# then gracefully restarts the photo-importer container to trigger a scan.

# Wait for the automount to complete
sleep 10

# Find the docker command and restart the container
# Using the container_name we set in our docker-compose file.
/usr/bin/docker restart photo-importer
