#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="bootstrap"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

ABS_PATH=$(readlink -f "$0")
BIN_DIR=$(dirname $ABS_PATH)

# Read in Variables from .env file
export $(grep -v '^#' .env | xargs)

# Login to ECR, to log into ECR you need AWS variables set
source "$BIN_DIR/ecr/login"

# Set Bin Path to allow CFN-Guard to run
export PATH=~/.guard/bin:$PATH