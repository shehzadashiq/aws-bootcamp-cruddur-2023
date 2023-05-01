#!/usr/bin/bash

# Initialise session manager
# Get the absolute path of this script
ABS_PATH=$(readlink -f "$0")
ECS_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $ECS_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)

echo $PROJECT_PATH

sudo dpkg -i $PROJECT_PATH/session-manager-plugin.deb