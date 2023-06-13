#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CYAN='\033[1;36m'
NO_COLOR='\033[0m'

# Get the absolute path of this script
ABS_PATH=$(readlink -f "$0")
CFN_BIN_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $CFN_BIN_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
FUNC_DIR="$PROJECT_PATH/aws/lambdas/cruddur-messaging-stream/"
TEMPLATE_PATH="$PROJECT_PATH/aws/cfn/ddb/template.yaml"
CONFIG_PATH="$PROJECT_PATH/aws/cfn/ddb/config.toml"
ARTIFACT_BUCKET="cfn-tajarba-artifacts"
echo $TEMPLATE_PATH

sam validate -t $TEMPLATE_PATH

LABEL="SAM_BUILD"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html
# --use-container
# use container is for building the lambda in a container
# it's still using the runtimes and its not a custom runtime
sam build \
--use-container \
--config-file $CONFIG_PATH \
--template $TEMPLATE_PATH \
--base-dir $FUNC_DIR \
--region $AWS_DEFAULT_REGION
#--parameter-overrides

TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/template.yaml"
OUTPUT_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"

LABEL="SAM_PACKAGE"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-package.html
sam package \
  --s3-bucket $ARTIFACT_BUCKET \
  --config-file $CONFIG_PATH \
  --template $TEMPLATE_PATH \
  --output-template-file $OUTPUT_TEMPLATE_PATH \
  --s3-prefix "ddb"

LABEL="SAM_DEPLOY"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

PACKAGED_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"

# # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html
sam deploy \
  --template-file $PACKAGED_TEMPLATE_PATH  \
  --config-file $CONFIG_PATH \
  --stack-name "CrdDdb" \
  --tags group=cruddur-ddb \
  --capabilities "CAPABILITY_NAMED_IAM"
