#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="bootstrap"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

ABS_PATH=$(readlink -f "$0")
BIN_PATH=$(dirname $ABS_PATH)
DB_PATH="$BIN_PATH/db"
DDB_PATH="$BIN_PATH/ddb"
echo "====$"
echo $DB_PATH
echo "====$"

source "$DB_PATH/create.sh"
source "$DB_PATH/schema-load.sh"
source "$DB_PATH/seed.sh"
python "$DB_PATH/update_cognito_user_ids.py"
python "$DDB_PATH/schema-load.py"
python "$DDB_PATH/seed.py"