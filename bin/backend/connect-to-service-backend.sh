#!/usr/bin/bash
CLUSTER_NAME=CrdClusterFargateCluster
SERVICE_NAME=backend-flask
CONTAINER_NAME=backend-flask

export TASK_ID=$(aws ecs list-tasks --cluster $CLUSTER_NAME --service-name $SERVICE_NAME --query 'taskArns[*]' --output json | jq -r 'join(",")')

echo "TASK ID : $TASK_ID"
echo "Container Name: $CONTAINER_NAME"

aws ecs execute-command  \
--region $AWS_DEFAULT_REGION \
--cluster $CLUSTER_NAME \
--task $TASK_ID \
--container $CONTAINER_NAME \
--command "/bin/bash" \
--interactive