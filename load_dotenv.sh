#! /usr/bin/bash

# set -o allexport; source .env; set +o allexport
export $(grep -v '^#' .env | xargs)
