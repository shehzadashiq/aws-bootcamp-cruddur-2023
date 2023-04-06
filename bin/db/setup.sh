#! /usr/bin/bash
-e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

# bin_path="$(realpath .)/bin"
ABS_PATH=$(readlink -f "$0")
DB_PATH=$(dirname $ABS_PATH)

source "$DB_PATH/drop"
source "$DB_PATH/create"
source "$DB_PATH/schema-load"
source "$DB_PATH/seed"
python "$DB_PATH/update_cognito_user_ids"


# NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
# psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"

