## Architecture Guide

Before you run any templates, be sure to create an S3 bucket to contain
all of our artifacts for CloudFormation.

```sh
export CFN_BUCKET="cfn-tajarba-artifacts"
gp env CFN_BUCKET=$CFN_BUCKET
aws s3api create-bucket \
    --bucket $CFN_BUCKET \
    --region $AWS_DEFAULT_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_DEFAULT_REGION
```

> remember bucket names are unique to the provide code example you may need to adjust