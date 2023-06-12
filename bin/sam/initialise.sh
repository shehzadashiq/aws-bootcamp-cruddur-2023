#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="SAM Initialise"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

cd /workspace
sudo ./sam-installation/install
cd $THEIA_WORKSPACE_ROOT