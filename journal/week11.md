# Week 11/X — CloudFormation Part 2 - Cleanup

## Overview

Due to scope creep, this week will focus on cleaning up the code and ensuring it is in a stable state.

## Videos for week X

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

## Week X Sync tool for static website hosting

Create a bucket to host the frontend

`aws s3 mb s3://tajarba.com`

Create the following scripts `static-build` and `sync` in `bin/frontend` and set them as executable

```sh
touch bin/frontend/static-build
touch bin/frontend/sync
chmod u+x bin/frontend/static-build
chmod u+x bin/frontend/sync
```

Create a new file `erb/sync.env.erb` that holds the environment variables for the `bin/frontend/sync` script

```sh
touch erb/sync.env.erb
```

Add the following, replace `SYNC_S3_BUCKET` and `SYNC_CLOUDFRONT_DISTRIBUTION_ID` with your own.

```erb
SYNC_S3_BUCKET=tajarba.com
SYNC_CLOUDFRONT_DISTRIBUTION_ID=ELTQ0Y5RKUKSF
SYNC_BUILD_DIR=<%= ENV['THEIA_WORKSPACE_ROOT'] %>/frontend-react-js/build
SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp/changeset.json
SYNC_AUTO_APPROVE=false
```

Create the following files in the root of the repository

- Gemfile
- Rakefile

```sh
touch Gemfile
touch Rakefile
```

The code for these files is located respectively here [Gemfile](../Gemfile) and here [Rakefile](../Rakefile).

Create the following file `./tmp/.keep` as a placeholder

```sh
touch tmp/.keep
```

Create a `sync` script in `bin/cfn`

```sh
touch bin/cfn/sync
chmod u+x bin/cfn/sync
```

Update `bin/cfn/sync` with the following [code](../bin/cfn/sync)

### Create Sync Template

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/sync
touch aws/cfn/sync/template.yaml aws/cfn/sync/config.toml aws/cfn/sync/config.toml.example
```

Update config.toml with the following settings that specify the bucket, region and name of the CFN stack. Replace `bucket` and `region` with your own.

We also need to specify the GitHubOrg which in our case will correspond to our GitHub username and the GitHub Repository name

```toml
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdSyncRole'

[parameters]
GitHubOrg = 'shehzadashiq'
RepositoryName = 'aws-bootcamp-cruddur-2023'
OIDCProviderArn = ''
```

Update `aws/cfn/sync/template.yaml` with the following [code](../aws/cfn/sync/template.yaml)

## Troubleshooting

### AWS CLI Issues

In GitPod, docker compose started to fail with the following message

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3b13d8e5-fceb-4d14-b21e-05830ddba6a2)

I noticed that tasks within Gitpod.yml were not working either. The same issue happened in a new environment

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/6a86a4c6-45c7-4d94-9243-d0f5c804b522)

The following error was shown

`Could not connect to the endpoint URL: "http://dynamodb-local:8000/"`

I looked further into the error and saw that the value was configured as an environment variable `AWS_ENDPOINT_URL` when we were using DynamoDB in week 5 locally. This had not caused any issues previously so I was surprised that this had happened.

To resolve this issue I unset the variable locally and removed it from Gitpod

```sh
gp env -u AWS_ENDPOINT_URL
unset AWS_ENDPOINT_URL
```

Once this had been unset I was able to run all aws_cli commands and run docker-compose
