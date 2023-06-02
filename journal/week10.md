# Week 10 — CloudFormation Part 1

- [Overview](#overview)
- [Pre-Requisites](#pre-requisites)
- [CFN Networking Stack](#cfn-networking-stack)
- [Journal Summary](#journal-summary)

---

## Overview

### Videos for week 10

- [CFN For Networking Layer](https://www.youtube.com/watch?v=jPdm0uLyFLM)
- [CFN Diagramming the Network Layer](https://www.youtube.com/watch?v=lb3aKVVMn7U)
- [CFN Cluster Layer](https://www.youtube.com/watch?v=lb3aKVVMn7U)
- [CFN Toml Part 1](https://www.youtube.com/watch?v=ATv1Z-T0LKI)
- [CFN Toml Part 2](https://www.youtube.com/watch?v=cYoNAadSYM8)
- [CFN Cluster Layer Finish](https://www.youtube.com/watch?v=RITT94dfhOM)
- [CFN Diagram Cluster](https://www.youtube.com/watch?v=cNFr8bvM100)
- [CFN Toml Part 1](https://www.youtube.com/watch?v=ATv1Z-T0LKI)
- [CFN Toml Part 2](https://www.youtube.com/watch?v=cYoNAadSYM8)
- [CFN Cluster Layer Finish](https://www.youtube.com/watch?v=RITT94dfhOM)
- [CFN Diagram Cluster](https://www.youtube.com/watch?v=cNFr8bvM100)
- [CFN Service Layer](https://www.youtube.com/watch?v=yj8QK8YULCQ)
- [CFN ECS Fargate Service Debugging](https://www.youtube.com/watch?v=ERfSZy2Mpw4)
- [CFN ECS Faragate Service Debugging Further](https://www.youtube.com/watch?v=FgCKWtVm8mE)
- [CFN RDS](https://www.youtube.com/watch?v=BNZfYl_82ZU)
- [CFN RDS Finish](https://www.youtube.com/watch?v=kBR9tlwbiyA)
- [CFN Service Attempt Again](https://www.youtube.com/watch?v=hCGIbMOtkIc)
- [CFN Service Fixed](https://www.youtube.com/watch?v=ozzL2Hqn3Ms)
- [CFN Service Confirmed Fixed](https://www.youtube.com/watch?v=GbhSmuTpRtE)
- [CFN - Diagramming Service and RDS](https://www.youtube.com/watch?v=y6ShAco6Edg)
- [SAM CFN for Dynamodb DynamoDB Streams Lambda](https://www.youtube.com/watch?v=8UGa4q-zRJ8)
- [SAM CFN Fix SAM Lambda Code Artifact](https://www.youtube.com/watch?v=XUUpoBGgNQI)
- [Diagramming DynamoDB](https://www.youtube.com/watch?v=ZK5PdSbxpH0)
- [CFN CICD Part 1](https://www.youtube.com/watch?v=8EY4UwON7y8)
- [CFN CICD Part 2](https://www.youtube.com/watch?v=P_QbQV0JyJc)
- [CFN Diagramming CICD](https://www.youtube.com/watch?v=bmS-z2J7oTs)
- [CFN Static Website Hosting Frontend](https://www.youtube.com/watch?v=Qc96g_blibA)
- [CFN Diagramming Static Frontend](https://www.youtube.com/watch?v=IEBHegBqne0)
- [Week X Sync tool for static website hosting](https://www.youtube.com/watch?v=0nDBqZGu4rI)
- [Week X Reconnect Database and Post Confirmation Lambda](https://www.youtube.com/watch?v=gukwarWjc4o)
- [Week X Use CORS for Service](https://www.youtube.com/watch?v=f0aLm0EpzaE)
- [Week-X CICD Pipeline and Create Activity](https://www.youtube.com/watch?v=H9-9gR604L4)
- [Week-X Refactor JWT to use a decorator](https://www.youtube.com/watch?v=4lHRwJ0yzpo)
- [Week-X Refactor AppPy](https://www.youtube.com/watch?v=VSVb_-6zYaY)
- [Week-X Refactor Flask Routes](https://www.youtube.com/watch?v=INkTj-Ark7k)
- [Week-X Replies Work In Progress](https://www.youtube.com/watch?v=qXxYF4y0gJ8&)
- [Week-X Refactor Error Handling and Fetch Requests](https://www.youtube.com/watch?v=rFcPG6e_kGs)
- [Week-X Activity Show Page](https://www.youtube.com/watch?v=FBpQtN497QA)
- [Week-X Cleanup](https://www.youtube.com/watch?v=E89RBvZ_BaY)
- [Week X Cleanup Part 2](https://www.youtube.com/watch?v=53_3TmZ1hrs)

### References

[Andrew's Notes](https://github.com/omenking/aws-bootcamp-cruddur-2023/tree/week-10-again/aws/cfn)
[Task Definition](https://gist.github.com/omenking/6564ad312cb9398ad5427204253cfed5)
[CIDR.xyz](https://cidr.xyz/)

### AWS Documentation

[AWS::EC2::VPC](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html)

---

## Pre-Requisites

- AWS CloudFormation Guard Installation
- S3 Bucket to contain artifacts
- CFN-TOML installation

### AWS CloudFormation Guard Installation

[AWS CloudFormation Guard](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html) is a policy-as-code evaluation tool.

```sh
pip install cfn-lint
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/aws-cloudformation/cloudformation-guard/main/install-guard.sh | sh
export PATH=~/.guard/bin:$PATH
gem install cfn-toml
```

Verify installation was successful by running `cfn-guard --version`

If successful, similar output should be shown `cfn-guard 2.1.3`

[Windows Installation](https://docs.aws.amazon.com/cfn-guard/latest/ug/setting-up-windows.html) requires VS Code 2019 Build Tools, Rust Package Manager to be installed before it can be used.

### Create S3 Bucket for artifacts

All S3 buckets have unique global names. When creating your bucket choose your own. Regions outside of `us-east-1` require the appropriate `LocationConstraint` to be specified in order to create the bucket in the desired region

```sh
export CFN_BUCKET="cfn-tajarba-artifacts"
gp env CFN_BUCKET=$CFN_BUCKET
aws s3api create-bucket \
    --bucket $CFN_BUCKET \
    --region $AWS_DEFAULT_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_DEFAULT_REGION
```

### CFN-Toml installation

[CFN-TOML](https://github.com/teacherseat/cfn-toml) will read a toml file that is designed to be used with CloudFormation CLI commands within a bash script.

Installation is performed by

`gem install cfn-toml`

### Modify Bootstrap.sh to install CFN packages (Optional)

Gitpod was not initialising the CFN section of the gitpod.yml all the time. To automate this I created a script `bin/cfn/initialise.sh`

```sh
touch bin/cfn/initialise.sh
chmod u+x bin/cfn/initialise.sh
```

This script installs all the required Python and Ruby packages. It's contents are shown below

```sh
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="CFN Initialise"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

pip install cfn-lint
cargo install cfn-guard
gem install cfn-toml
```

This was then referenced in `bin/bootstrap` thus.

```sh
# Install CFN section
source "$BIN_DIR/cfn/initialise.sh"
```

---

## CFN Networking Stack

### Create Networking Template

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/networking
cd aws/cfn/networking
touch template.yaml config.toml.example config.toml
```

Update config.toml with the following settings that specify the bucket, region and name of the CFN stack.

```toml
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdNet'
```

### Create Networking Deploy Script

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch networking-deploy
chmod u+x networking-deploy
```

I modified the script to not have hardcoded values as I am using my local machine and GitPod for development.

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="CFN_NETWORK_DEPLOY"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

# Get the absolute path of this script
ABS_PATH=$(readlink -f "$0")
CFN_BIN_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $CFN_BIN_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
CFN_PATH="$PROJECT_PATH/aws/cfn/networking/template.yaml"
CONFIG_PATH="$PROJECT_PATH/aws/cfn/networking/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix networking \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-networking \
  --capabilities CAPABILITY_NAMED_IAM
```

Running `./bin/cfn/networking-deploy` now initiates a changeset for the CFN stack.

CLI Output of running `./bin/cfn/networking-deploy`
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3f7eabd7-7d1f-44d4-ac4e-ceb0b4659033)

#### Proof of Stack Creation

##### Stack Ready to be reviewed

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/b57ec7e8-6476-4cfa-bd20-7a19714bdfad)

##### Change Set Created

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/e0290e88-0913-47c5-ab56-887ca3f3de68)

##### Change Set ready to be executed
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/adc53128-4dd0-44ca-8022-f1b3dbf33353)

##### Execute Change Set
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/eb0b4b6b-3b44-47f3-aecb-144802c4b6ae)

##### Creation in Progress
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/d30b36b0-3cb0-4af4-afeb-6a6b093411b7)

##### Stack Creation Events
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/954f9831-0d84-4721-8e09-a6015fef249b)

##### Stack Overview Once completed
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/35e15cb7-9126-4538-b17f-7b4d94575206)

##### Stack Parameters used during Creation
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/a31d7e7a-a74f-439d-8443-ccf91f2d138f)

##### Stack Resources
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/a8778a82-e75c-4c34-a28b-aae5de2eda77)

##### Stack Outputs
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/799e02b8-670b-41ce-ab49-63c969ef5f94)

##### Stack Change Set
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/bd9fa40c-2cfe-441d-afc3-f2a070eaea58)

##### Stack Created Successfully
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3a2d192d-a9f5-42e3-a67c-d24be4a1759e)

---

## CFN Cluster Stack

This stack builds upon our networking stack and takes the output from it to build our cluster. It specifically requires the ARN of our domain certificate to create a HTTPS listener and the name of our networking stack to be able to reference its outputs (Public Subnets etc.).

### Create Cluster Template

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/cluster
cd aws/cfn/cluster
touch template.yaml config.toml config.toml.example
```

### Create Cluster Deploy Script

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch cluster-deploy
chmod u+x cluster-deploy
```

## CFN Service Stack

### Create Service Template

As I did with the networking-deploy script I modified the script to not have hardcoded values.


```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/networking
cd aws/cfn/networking
touch template.yaml config.toml.example config.toml
```

Update config.toml with the following settings that specify the bucket, region and name of the CFN stack.

```toml
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdNet'
```

### Create Networking Deploy Script

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch networking-deploy
chmod u+x networking-deploy
```

I modified the script to not have hardcoded values as I am using my local machine and GitPod for development.

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="CFN_NETWORK_DEPLOY"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

# Get the absolute path of this script
ABS_PATH=$(readlink -f "$0")
CFN_BIN_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $CFN_BIN_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
CFN_PATH="$PROJECT_PATH/aws/cfn/networking/template.yaml"
CONFIG_PATH="$PROJECT_PATH/aws/cfn/networking/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix networking \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-networking \
  --capabilities CAPABILITY_NAMED_IAM
```

Running `./bin/cfn/networking-deploy` now initiates a changeset for the CFN stack.

---

## CFN DB Stack

This instance is needed before the service can be created.



---

## Spend Issue

I received an alert that my ELB spend will exceed the free tier elements.

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/42ce4741-182b-4a41-aeef-bf8f1338f229)

It turned out that the Cruddur cluster created using the ECS tasks had been running since September. As it was not needed I removed it using a script. 

'/workspace/aws-bootcamp-cruddur-2023/bin/ecs/cluster-delete.sh'

The script cycles through both the frontend/backend tasks and then deletes all services before deleting them.

```sh
#! /usr/bin/bash

CLUSTER_NAME="cruddur"

# Deregister frontend first
SERVICE_NAME="frontend-react-js"
TASK_DEFINTION_FAMILY="frontend-react-js"

LATEST_TASK_DEFINITION_ARN=$(aws ecs describe-task-definition \
--task-definition $TASK_DEFINTION_FAMILY \
--query 'taskDefinition.taskDefinitionArn' \
--output text)

echo "TASK DEF ARN:"
echo $LATEST_TASK_DEFINITION_ARN

# Deregister task first
aws ecs deregister-task-definition --task-definition $LATEST_TASK_DEFINITION_ARN

# Deregister backend next
SERVICE_NAME="backend-flask"
TASK_DEFINTION_FAMILY="backend-flask"

LATEST_TASK_DEFINITION_ARN=$(aws ecs describe-task-definition \
--task-definition $TASK_DEFINTION_FAMILY \
--query 'taskDefinition.taskDefinitionArn' \
--output text)

echo "TASK DEF ARN:"
echo $LATEST_TASK_DEFINITION_ARN

# Deregister task
aws ecs deregister-task-definition --task-definition $LATEST_TASK_DEFINITION_ARN

# Scale down all services in the cluster now that tasks have been deregistered
for service in $(aws ecs list-services --cluster $CLUSTER_NAME --output text | awk '{print $2}'); do aws ecs update-service --cluster $CLUSTER_NAME --service $service --desired-count 0; done

# List all services in the cluster
aws ecs list-services --cluster $CLUSTER_NAME --output text

# Describe the services
for service in $(aws ecs list-services --cluster $CLUSTER_NAME --output text | awk '{print $2}'); do aws ecs describe-services --cluster $CLUSTER_NAME --service $service; done

# Delete services
for service in $(aws ecs list-services --cluster $CLUSTER_NAME --output text | awk '{print $2}'); do aws ecs delete-service --cluster $CLUSTER_NAME --service $service; done

# Delete cluster
aws ecs delete-cluster --cluster $CLUSTER_NAME
```

## Journal Summary
