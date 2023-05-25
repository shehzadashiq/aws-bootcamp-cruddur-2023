#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="CFN Initialise"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

pip install cfn-lint
cargo install cfn-guard
gem install cfn-toml