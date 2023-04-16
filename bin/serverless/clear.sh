#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
SERVERLESS_PATH=$(dirname $ABS_PATH)
DATA_FILE_PATH="$SERVERLESS_PATH/files/data.jpg"

# aws s3 rm "s3://cruddur-uploaded-avatars/avatars/original/data.jpg"
aws s3 rm "s3://assets.$DOMAIN_NAME/avatars/original/data.png"
aws s3 rm "s3://assets.$DOMAIN_NAME/avatars/processed/data.png"