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

---

## CFN Networking Stack

### Create Networking Template

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/networking
cd aws/cfn/networking
touch template.yaml config.toml.example
```

### Create Networking Deploy

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch networking-deploy
chmod u+x networking-deploy
```

## Journal Summary
