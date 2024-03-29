# Week 10 — CloudFormation Part 1

- [Week 10 — CloudFormation Part 1](#week-10--cloudformation-part-1)
  - [Overview](#overview)
    - [Videos for week 10](#videos-for-week-10)
    - [References](#references)
    - [AWS Documentation](#aws-documentation)
  - [Pre-Requisites](#pre-requisites)
    - [AWS CloudFormation Guard Installation](#aws-cloudformation-guard-installation)
    - [Create S3 Bucket for artifacts](#create-s3-bucket-for-artifacts)
    - [CFN-Toml installation](#cfn-toml-installation)
    - [Modify Bootstrap.sh to install CFN packages (Optional)](#modify-bootstrapsh-to-install-cfn-packages-optional)
  - [CFN Networking Stack](#cfn-networking-stack)
    - [Create Networking Template](#create-networking-template)
    - [Create Networking Deploy Script](#create-networking-deploy-script)
      - [Proof of Stack Creation](#proof-of-stack-creation)
        - [Stack Ready to be reviewed](#stack-ready-to-be-reviewed)
        - [Change Set Created](#change-set-created)
        - [Change Set ready to be executed](#change-set-ready-to-be-executed)
        - [Execute Change Set](#execute-change-set)
        - [Creation in Progress](#creation-in-progress)
        - [Stack Creation Events](#stack-creation-events)
        - [Stack Overview Once completed](#stack-overview-once-completed)
        - [Stack Parameters used during Creation](#stack-parameters-used-during-creation)
        - [Stack Resources](#stack-resources)
        - [Stack Outputs](#stack-outputs)
        - [Stack Change Set](#stack-change-set)
        - [Stack Created Successfully](#stack-created-successfully)
  - [CFN Cluster Stack](#cfn-cluster-stack)
    - [Create Cluster Template](#create-cluster-template)
    - [Create Cluster Deploy Script](#create-cluster-deploy-script)
  - [CFN Service Stack](#cfn-service-stack)
    - [Create Service Template](#create-service-template)
  - [CFN DB Stack](#cfn-db-stack)
    - [Create DB Template](#create-db-template)
    - [Create DB Deploy Script](#create-db-deploy-script)
    - [Seed DB](#seed-db)
  - [CFN DDB Stack](#cfn-ddb-stack)
    - [Create DDB Template](#create-ddb-template)
    - [Create DDB Deploy Script](#create-ddb-deploy-script)
    - [Create Service Deploy Script](#create-service-deploy-script)
  - [CFN MachineUser Stack](#cfn-machineuser-stack)
    - [Create MachineUser Template](#create-machineuser-template)
    - [Script to allow access from GitPod](#script-to-allow-access-from-gitpod)
    - [Create MachineUser Deploy Script](#create-machineuser-deploy-script)
  - [CFN Frontend Stack](#cfn-frontend-stack)
    - [Create Frontend Template](#create-frontend-template)
  - [Troubleshooting](#troubleshooting)
    - [Changes need to DB SG once the stack has been created](#changes-need-to-db-sg-once-the-stack-has-been-created)
    - [Domain not resolving](#domain-not-resolving)
    - [503 Error being shown once stack has been deployed](#503-error-being-shown-once-stack-has-been-deployed)
    - [CFN Service Stack Issue](#cfn-service-stack-issue)
      - [Summary](#summary)
      - [Troubleshooting Stack Issue](#troubleshooting-stack-issue)
    - [Spend Issue](#spend-issue)
  - [Journal Summary](#journal-summary)
    - [CFN Stacks Created](#cfn-stacks-created)
  - [Diagram for Week 10](#diagram-for-week-10)
    - [CFN Networking Layer Diagram](#cfn-networking-layer-diagram)
    - [CI/CD Layer Diagram Detail](#cicd-layer-diagram-detail)
    - [Route53/Cloudfront Layer Diagram Detail](#route53cloudfront-layer-diagram-detail)
    - [Architectural Diagram Overview](#architectural-diagram-overview)
    - [Architectural Diagram](#architectural-diagram)

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

### References

[Andrew's Notes](https://github.com/omenking/aws-bootcamp-cruddur-2023/tree/week-10-again/aws/cfn)
[Task Definition](https://gist.github.com/omenking/6564ad312cb9398ad5427204253cfed5)
[CIDR.xyz](https://cidr.xyz/)

### AWS Documentation

[AWS::EC2::VPC](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html)

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

## CFN DB Stack

### Create DB Template

As I did with the networking-deploy script I modified the script to not have hardcoded values.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/db
cd aws/cfn/db
touch template.yaml config.toml.example config.toml
```

Update config.toml with the following settings that specify the bucket, region and name of the CFN stack.

```toml
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdDb'

[parameters]
NetworkingStack = 'CrdNet'
ClusterStack = 'CrdCluster'
MasterUsername = 'cruddurroot'
```

### Create DB Deploy Script

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch db-deploy
chmod u+x db-deploy
```

Update the script with the following [code](../bin/cfn/db-deploy)

### Seed DB

Before seeding we need to update the value for `PROD_CONNECTION_URL` to our new database. I updated it in both Parameter Store and GitPod.

We need to update it both locations because a connection will be made by the application `/cruddur/backend-flask/CONNECTION_URL` in parameter store. The GitPod `PROD_CONNECTION_URL` needs to be updated to allow seeding.

Once `PROD_CONNECTION_URL` has been set correctly, seed the database with data by running the following.

`./bin/db/setup prod`

## CFN DDB Stack

### Create DDB Template

### Create DDB Deploy Script

- Create `.aws-sam` with `./bin/cfn/ddb-build`
- Package with `./bin/cfn/ddb-package`
- Create CFN stack with inally `./bin/cfn/ddb-deploy`, in order to create CrdDdb stack.

The DDB table created now needs to be added to the following location `/aws/cfn/service/config.toml` and should look as below. Update the parameters for your domain and DDBMessageTable is obtained from the resources section of `CrdDdb`

```config
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdSrvBackendFlask'

[parameters]
EnvFrontendUrl = 'https://tajarba.com'
EnvBackendUrl = 'https://api.tajarba.com'
DDBMessageTable = 'CrdDdb-DynamoDBTable-1NK2LU7KGZSIP'
```

Update `aws/cfn/service/template.yaml`

Place this entry under parameters

```yaml
  DDBMessageTable:
    Type: String
    Default: cruddur-messages
```

The following needs to be added to the `Environment:` section under `TaskDefinition:`

```yaml
            - Name: DDB_MESSAGE_TABLE
              Value: !Ref DDBMessageTable       
```

Execute `./bin/cfn/service-deploy` to update `CrdSrvBackendFlask` with the DDB entry.

### Create Service Deploy Script

With all the pre-requisites in place the service stack can now be created.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch service-deploy
chmod u+x service-deploy
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

Running `./bin/cfn/service-deploy` now initiates a changeset for the CFN stack.

## CFN MachineUser Stack

### Create MachineUser Template

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/machine-user
cd aws/cfn/machine-user
touch template.yaml config.toml
```

Update `aws/cfn/machine-user/template.yaml` with the following code.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  CruddurMachineUser:
    Type: "AWS::IAM::User"
    Properties:
      UserName: "cruddur_machine_user"
  DynamoDBFullAccessPolicy:
    Type: "AWS::IAM::Policy"
    Properties:
      PolicyName: "DynamoDBFullAccessPolicy"
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Action:
              - dynamodb:PutItem
              - dynamodb:GetItem
              - dynamodb:Scan
              - dynamodb:Query
              - dynamodb:UpdateItem
              - dynamodb:DeleteItem
              - dynamodb:BatchWriteItem
            Resource: "*"
      Users:
        - !Ref CruddurMachineUser
```

Update config.toml with the following changing `bucket` and `region` as appropriate

```config
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdMachineUser'
```

### Script to allow access from GitPod

Similar to the `update-sg-rule` script used to allow access to the RDS database I created a script that will automatically update the `CrdDbRDSSG` security group with our GitPod IP. I then included this in both my `.gitpod.yml` and `./bin/bootstrap` script.

```sh
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="ddb-update-sg-rule"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"


SG_GROUP_NAME="CrdDbRDSSG"
GITPOD_IP=$(curl ifconfig.me)
echo $GITPOD_IP

# aws ec2 describe-vpcs --filters "Name=tag:Name,Values=CrdNetVPC"
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=CrdNetVPC" --query 'Vpcs[*].VpcId' --output text) 
echo $VPC_ID

# As the Security group is not in the default VPC we need to filter on both the VPC_ID and Security Group Name
DB_SG_ID=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=$SG_GROUP_NAME" --query 'SecurityGroups[*].GroupId' --output text)
echo $DB_SG_ID

# For now this is hard coded but figure a way to automate this
DB_SG_RULE_ID="sgr-099f9e3d8c8c1327e"

aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
 --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GitPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

### Create MachineUser Deploy Script

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch machineuser-deploy
chmod u+x machineuser-deploy
```

Update the script with the following [code](../bin/cfn/machineuser-deploy)

Running `./bin/cfn/machineuser-deploy` now initiates a changeset for the CFN stack.

## CFN Frontend Stack

### Create Frontend Template

To be written up as I missed documenting this.

## Troubleshooting

### Changes need to DB SG once the stack has been created

To allow connectivity from Gitpod and my desktop extra rules to allow traffic on port 5432 needed to be created in `CrdDbRDSSG`. Without this rule connections would fail.

### Domain not resolving

Once the service stack was deployed successfully it shows 200 in its logs

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/0f93e6da-65f2-473f-8d93-a529bba3854c)

However, trying to access <https://api.tajarba.com/api/health-check> would result in the following error `ERR_NAME_NOT_RESOLVED`

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/c7d45cf7-4174-4fe5-ae23-1455b97e11ab)

This is because in Route53, the A record for `api.tajarba.com` needed to be changed. Here we can see it is pointing to the old ALB which no longer exists

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/64585dd7-7173-4ee3-82ac-e98b2cf96fdd)

To verify which ALB was created by the cluster this can be seen in the resources created by the Cluster stack `CrdCluster`

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/4e678784-024e-4ae9-95d1-8fbf3df57c79)

This can be checked easily from the CLI too using the following AWS command

`aws elbv2 describe-load-balancers --names  CrdClusterALB  --query "LoadBalancers[0].DNSName" --output text`

### 503 Error being shown once stack has been deployed

Accessing  <https://api.tajarba.com/api/health-check> would show that the stack was successfully deployed however trying to access <https://api.tajarba.com/api/activities/home> would display a 503 error

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/73ee9d33-b2fb-4b39-9938-a0fcbd04ecd5)

This was because in the cluster stack `HTTP Host Header` had been set incorrectly in `aws/cfn/cluster/template.yaml`. This was changed from

```yaml
          HostHeaderConfig: 
            Values: 
              - api.cruddur.com
```

to

```yaml
          HostHeaderConfig: 
            Values: 
              - api.tajarba.com
```

### CFN Service Stack Issue

The application failed to start which meant the Service stack could not be deployed

#### Summary

. The pool-connect error was because in my db-connect URL I had forgotten to update the username from root to cruddurroot
. The 'KeyError: 'keys' | backend-flask' error was because I had made a mistake in my cognito variables correcting this fixed the issue
. The TaskFailedElb-Check error was because in the cluster template the healthcheck port needs to be changed from port 80 to 4567

#### Troubleshooting Stack Issue

Application failing to start

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/56c2fa89-819f-4928-8525-8821e6e33245)

```sh
6/3/2023, 7:01:54 AM GMT+1 | cognito_jwt_token = CognitoJwtToken( | backend-flask
6/3/2023, 7:01:54 AM GMT+1 | File "/backend-flask/lib/cognito_jwt_token.py", line 32, in __init__ | backend-flask
6/3/2023, 7:01:54 AM GMT+1 | self._load_jwk_keys() | backend-flask
6/3/2023, 7:01:54 AM GMT+1 | File "/backend-flask/lib/cognito_jwt_token.py", line 39, in _load_jwk_keys | backend-flask
6/3/2023, 7:01:54 AM GMT+1 | self.jwk_keys = response.json()["keys"] | backend-flask
6/3/2023, 7:01:54 AM GMT+1 | KeyError: 'keys' | backend-flask
```

This was caused by a mistake in the cognito variables. I had the incorrect value for `EnvAWSCognitoUserPoolId`.

Changing this resolved the issue.

ELB Health Check Failures
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/78174143-f152-4777-b38a-6f288c82a5c1)

Logs showed the following error

```sh
ConnectionRefusedError: [Errno 111] Connection refused
urllib3.exceptions.NewConnectionError: <botocore.awsrequest.AWSHTTPConnection object at 0x7f5a310e4970>: Failed to establish a new connection: [Errno 111] Connection refused
botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL: "http://127.0.0.1:2000/SamplingTargets"
```

To resolve this I overrode it first manually in the Console here by changing it to 4567 as mentioned by other bootcampers

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/2b6023c8-5a7c-49d1-b4a6-8661b8bcc395)

This allowed the service stack to be created successfully.

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/8fba5601-ed79-44df-80b0-ed8eb455a16f)

To automate this I changed the backend health check port from 80 to 4567 in `/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/template.yaml` from

```yaml
  BackendHealthCheckPort:
    Type: String
    Default: 80
```

to

```yaml
  BackendHealthCheckPort:
    Type: String
    Default: 4567
```

This took the deployment time from hours down to 7 minutes

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/0757cdc9-d106-459a-9236-b50a5da73945)

### Spend Issue

I received an alert that my ELB spend will exceed the free tier elements.

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/42ce4741-182b-4a41-aeef-bf8f1338f229)

It turned out that the Cruddur cluster created using the ECS tasks had been running since September. As it was not needed I removed it using a script.

`/workspace/aws-bootcamp-cruddur-2023/bin/ecs/cluster-delete.sh`

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

Homework was completed successfully.

### CFN Stacks Created

All stacks created

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3eb2c4cc-a29a-4c44-8e49-495a51d416b2)

## Diagram for Week 10

I created the diagram using Lucid. I had to upgrade to the paid plan to continue using its features. To view the full diagram the following link can be used however I have tried to provide snippets of the diagram here too as it might be difficult to see on screen due to its size.

<https://lucid.app/lucidchart/84e6711d-fb07-47d6-b274-06fd577fc550/edit?viewport_loc=-1533%2C979%2C2994%2C1677%2C0_0&invitationId=inv_f1c5ef59-17fa-426c-8007-6fb6aff8e8f4>

### CFN Networking Layer Diagram

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/c5963753-8f8e-4f46-ba9a-7426257633dc)

### CI/CD Layer Diagram Detail

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/955a7908-8b8b-4c67-9b7b-f6d6db4b7239)

### Route53/Cloudfront Layer Diagram Detail

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/cb853303-fca4-4032-b70c-5d6b34dd3e4f)

### Architectural Diagram Overview

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/89506a5c-149f-4a23-b711-03405cfb058d)

### Architectural Diagram

![CFN Network Layer](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/7958cdd2-c1a8-4677-b9f0-7d5aeb59de22)
