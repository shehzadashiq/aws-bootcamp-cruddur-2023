#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
SERVERLESS_PATH=$(dirname $ABS_PATH)
DATA_FILE_PATH="$SERVERLESS_PATH/files/data.jpg"

aws s3 cp "$DATA_FILE_PATH" "s3://$DOMAIN-uploaded-avatars/data.jpg"
aws s3 cp "$DATA_FILE_PATH" "s3://assets2.$DOMAIN_NAME/avatars/data.jpg"

