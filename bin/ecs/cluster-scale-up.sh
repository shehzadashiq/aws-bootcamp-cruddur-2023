#!/usr/bin/bash

# CLUSTER_NAME="cruddur"
CLUSTER_NAME="CrdClusterFargateCluster"

# Scale up all services in the cluster
for service in $(aws ecs list-services --cluster $CLUSTER_NAME --output text | awk '{print $2}'); do aws ecs update-service --cluster $CLUSTER_NAME --service $service --desired-count 1; done
