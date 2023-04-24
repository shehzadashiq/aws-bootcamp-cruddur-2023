#! /usr/bin/env bash
set -e

# CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml"
CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/template.yaml"

cfn-lint $CFN_PATH

aws cloudformation deploy \
    --stack-name "my-cluster" \
    --s3-bucket "cfn-artifacts-tajarba" \
    --template-file $CFN_PATH \
    --no-execute-changeset \
    --capabilities CAPABILITY_NAMED_IAM