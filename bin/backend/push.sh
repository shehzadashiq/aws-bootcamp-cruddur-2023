#! /usr/bin/bash

ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL

#sudo dpkg -i $THEIA_WORKSPACE_ROOT/session-manager-plugin.deb

docker tag backend-flask-prod:latest $ECR_BACKEND_FLASK_URL:latest

docker push $ECR_BACKEND_FLASK_URL:latest
