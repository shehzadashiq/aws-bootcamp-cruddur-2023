#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
SERVERLESS_PATH=$(dirname $ABS_PATH)
DATA_FILE_PATH="$SERVERLESS_PATH/files/data.jpg"

# aws s3 cp "$DATA_FILE_PATH" "s3://cruddur-uploaded-avatars/data.jpg"
aws s3 cp "$DATA_FILE_PATH" "s3://assets.$DOMAIN_NAME/avatars/original/data.jpg"