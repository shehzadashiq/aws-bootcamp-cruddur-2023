# Week 11/X — CloudFormation Part 2 - Cleanup

- [Week 11/X — CloudFormation Part 2 - Cleanup](#week-11x--cloudformation-part-2---cleanup)
  - [Overview](#overview)
  - [Videos for week X](#videos-for-week-x)
  - [CFN CI/CD Stack](#cfn-cicd-stack)
    - [Create CI/CD Template](#create-cicd-template)
  - [Week X Sync tool for static website hosting](#week-x-sync-tool-for-static-website-hosting)
    - [Pre-Requisites](#pre-requisites)
    - [Create Build scripts](#create-build-scripts)
    - [Create Sync Template](#create-sync-template)
  - [Initialise Static Hosting](#initialise-static-hosting)
    - [Run Static-Build script](#run-static-build-script)
    - [Initialise Sync](#initialise-sync)
  - [Create GitHub Action](#create-github-action)
    - [Failure on GitHub Actions](#failure-on-github-actions)
  - [CleanUp](#cleanup)
  - [Messaging Alt User](#messaging-alt-user)
  - [Allowing Production to upload images](#allowing-production-to-upload-images)
    - [CORS Amendments required to allow avatars to be uploaded to the S3 bucket](#cors-amendments-required-to-allow-avatars-to-be-uploaded-to-the-s3-bucket)
    - [PUT Method not allowed in application](#put-method-not-allowed-in-application)
  - [Troubleshooting](#troubleshooting)
    - [Issues](#issues)
    - [Issues during CI/CD stack deployment](#issues-during-cicd-stack-deployment)
  - [Update Lambda](#update-lambda)
    - [Add Rule to `CrdDbRDSSG` SG to allow connection from Lambda](#add-rule-to-crddbrdssg-sg-to-allow-connection-from-lambda)
    - [AWS CLI Issues](#aws-cli-issues)
    - [Bootstrap Script](#bootstrap-script)
    - [Warnings being shown when running static build](#warnings-being-shown-when-running-static-build)
  - [Proof of working in Production](#proof-of-working-in-production)
    - [Messaging to AltUser working in Prod](#messaging-to-altuser-working-in-prod)
    - [Cruds work in Prod](#cruds-work-in-prod)
    - [Replies working in Prod](#replies-working-in-prod)
    - [Profile Image successfully uploaded](#profile-image-successfully-uploaded)
    - [Bio Changed](#bio-changed)

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

## CFN CI/CD Stack

### Create CI/CD Template

Create the folder structure.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/cicd
cd aws/cfn/cicd
touch template.yaml config.toml
```

The CI/CD stack requires a nested codebuild stack so a directory needs to be created for it too.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/cicd/nested
cd aws/cfn/cicd/nested
touch codebuild.yaml
```

Update the files with the following code.

- ["aws/cfn/cicd/template.yaml"](../aws/cfn/cicd/template.yaml)
- ["aws/cfn/cicd/config.toml"](../aws/cfn/cicd/config.toml)
- ["aws/cfn/cicd/nested/codebuild.yaml"](../aws/cfn/cicd/nested/codebuild.yaml)

`aws/cfn/cicd/config.toml` structure

```toml
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdCicd'

[parameters]
ServiceStack = 'CrdSrvBackendFlask'
ClusterStack = 'CrdCluster'
GitHubBranch = 'prod'
GithubRepo = 'shehzadashiq/aws-bootcamp-cruddur-2023'
ArtifactBucketName = "codepipeline-cruddur-tajarba-artifacts"
BuildSpec = 'backend-flask/buildspec.yml'
```

## Week X Sync tool for static website hosting

### Pre-Requisites

- Publicly accessible bucket that was created via `./bin/cfn/frontend`
- Cloudfront distribution that was created via `./bin/cfn/frontend`

### Create Build scripts

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
SYNC_CLOUDFRONT_DISTRIBUTION_ID=E2VH3EBBB8C06D
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

## Initialise Static Hosting

### Run Static-Build script

Run build script `./bin/frontend/build` , you should see output similar to the following when successful.

```console
The build folder is ready to be deployed.
You may serve it with a static server:

  npm install -g serve
  serve -s build

Find out more about deployment here:

  https://cra.link/deployment
```

Change to the frontend directory and zip the build folder

```sh
cd frontend-react-js
zip -r build.zip build/
```

The steps within the video recommended downloading the zip file locally and then uploading it to the s3 bucket. I instead chose to use the [s3 cp](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html) command to copy from the `frontend-react-js` folder directly to the s3 bucket `s3://tajarba.com`

`aws s3 cp build  s3://tajarba.com/ --recursive`

I verified everything had been copied successfully using the `s3 ls` command

`aws s3 ls s3://tajarba.com`

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/cd6957a3-934d-47e7-bdbf-104d9978ac6c)

### Initialise Sync

In the root of the repository

- Install the pre-requisite ruby gems `gem install aws_s3_website_sync dotenv`
- Generate `sync.env` by running updated `./bin/frontend/generate-env`
- Initiate synchronisation './bin/frontend/sync'
- Create CFN Sync `CrdSyncRole` stack by running `./bin/cfn/sync`

Sync Executed
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/44c5f5d1-aaf6-4c75-843b-e0dec41a512a)

Invalidation Created
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/f9a94e28-efcc-461c-9ffc-442e0ab1e80b)

Invalidation Details
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/7e43586a-3768-4af4-8f4e-d8659b6d66da)

## Create GitHub Action

Create folder in base of repo for action

```sh
mkdir -p .github/workflows/
touch .github/workflows/sync.yaml
```

Update with the following. Replace `role-to-assume` with the role generated in `CrdSyncRole` and `aws-region` with the region your stack was created in.

```yaml
name: Sync-Prod-Frontend

on:
  push:
    branches: [ prod ]
  pull_request:
    branches: [ prod ]

jobs:
  build:
    name: Statically Build Files
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [ 18.x]
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: cd frontend-react-js
      - run: npm ci
      - run: npm run build
  deploy:
    name: Sync Static Build to S3 Bucket
    runs-on: ubuntu-latest
    # These permissions are needed to interact with GitHub's OIDC Token endpoint.
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Configure AWS credentials from Test account
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::797130574998:role/CrdSyncRole-Role-VW38RM6ZXJ6W
          aws-region: eu-west-2
      - uses: actions/checkout@v3
      - name: Set up Ruby
        uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: '3.1'
      - name: Install dependencies
        run: bundle install
      - name: Run tests
        run: bundle exec rake sync
```

### Failure on GitHub Actions

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/5a5ce4db-9517-4c48-8f4a-4c146b95fe37)

## CleanUp

This involved the following

- Refactoring of code
- Reimporting code from other branches that had been missed e.g. TimeDateCode
- Fixing CloudFormation stacks to correct missing settings
- Adding a user to ensure least privilege access
- Refactor to use JWT decorator in the application
- Implementing replies
- Improve error handling
- Other Quality Of Life Changes

## Messaging Alt User

I used the following URL to message my altUser in Production: `https://tajarba.com/messages/new/altshehzad`

## Allowing Production to upload images

To allow messaging, the following changes need to be made from my experience

- Update the CORS Policy for the avatars bucket to change the `AllowedOrigins` to the production domain
- In the CruddurAvatarUpload Lambda edit `function.rb` to the production domain. Make sure to not have a trailing slash i.e it should be `https://tajarba.com`
- Add the `PUT` method in `/api/profile/update` under `backend-flask/routes/users.py`
- Update the CORS Policy for the avatars bucket to change the `AllowedMethods` as `POST,PUT`

### CORS Amendments required to allow avatars to be uploaded to the S3 bucket

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3fba2205-b138-4050-9a29-b2e0d57836d3)

### PUT Method not allowed in application

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/a7245aef-adb6-4d2d-ad5e-d63c5160725d)

## Troubleshooting

### Issues

- Tasks in GitPod and AWS CLI stopped running because `AWS_ENDPOINT_URL` had been set and was causing issues
- CI/CD configuration error
- Reply function not working due to code overwrite error, specifically I had when copy/pasting code and not realising this. I ended up having to spend time trying to figure out what the issue was by debugging
- Rollbar stopped working despite working earlier with no errors thrown.
- Earlier on in the bootcamp I changed my seed script to include the BIO column so I do not need to run the migrations script
- Gitpod.yml would not always work. To resolve this I created a bootstrap script which automated the common tasks for me. This also worked in my local environment
- To save costs in Week 10, I had tore down the CFN stacks. This meant in WeekX I could no longer remember which stacks needed to exist as I had not yet finished documentation. Troubleshooting this consumed a lot of time.
- Uploading in production was causing CORS issues. In addition to adding permissions to the `tajarba.com` domain, this was resolved by adding the `PUT` method in `/api/profile/update` under `backend-flask/routes/users.py`

### Issues during CI/CD stack deployment

Error on First Run as Pipeline Execution Fails

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/5271a2c0-a2ff-46a6-915e-13a229a4be30)

Connection shows as pending
![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/15c1b50a-ab5f-43e8-bd30-6e277c4f9c61)

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/0d30d475-0df3-4f5d-ade6-154b6779fda5)

Choose Connection Application and click connect
![image]<https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/dd3d062e-0390-4a76-a97d-85b8a3719906>

Connection created successfully
![image]<https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/99575532-7849-4c6c-aba5-2516b240f6b9>

Pipeline still fails saying `[GitHub] No Branch [prod] found for FullRepositoryName [aws-bootcamp-cruddur-2023]`

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/1e47f990-e121-43ee-bf73-cce9245322dd)

When trying to edit the pipeline the following message is displayed `A repository Id must be in the format <account>/<repository-name>`

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/402dd34b-8d7a-4e4a-98f7-b302a61dcb32)

To resolve this change the following setting `GithubRepo` in `aws/cfn/cicd/config.toml` to include the account name e.g

`GithubRepo = 'shehzadashiq/aws-bootcamp-cruddur-2023'`

Pipeline failing at Build stage with error

`Error calling startBuild: Project cannot be found: arn:aws:codebuild:eu-west-2:797130574998:project/CrdCicd-CodeBuildBakeImageStack-1O32P0X7I5NBCProject (Service: AWSCodeBuild; Status Code: 400; Error Code: ResourceNotFoundException; Request ID: 3f7509fa-14e3-478b-9139-2ff5621ccc6e; Proxy: null)`

Build succeeded after updating with reference to codebuild and buildspec.yml

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/f66ec8cb-7145-461c-b515-8bb32aa5cc00)

## Update Lambda

A new security group was created for the Post Confirmation Lambda.

In `CrdDbRDSSG` created a rule to allow connectivity as it was previously connected to the default VPC.

### Add Rule to `CrdDbRDSSG` SG to allow connection from Lambda

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/355867f4-be73-489e-8c45-319bd6816448)

### AWS CLI Issues

In GitPod, docker compose started to fail with the following message

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3b13d8e5-fceb-4d14-b21e-05830ddba6a2)

I noticed that tasks within Gitpod.yml were not working either. The same issue happened in a new environment

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/6a86a4c6-45c7-4d94-9243-d0f5c804b522)

The following error was shown

`Could not connect to the endpoint URL: "http://dynamodb-local:8000/"`

I looked further into the error and saw that the value was configured as an environment variable `AWS_ENDPOINT_URL` when we were using DynamoDB in week 5 locally.

This was configured thus, `AWS_ENDPOINT_URL="http://dynamodb-local:8000"`

This had not caused any issues previously so I was surprised that this had happened.

I tried to change the URL to point to my region following the recommendations here <https://docs.aws.amazon.com/general/latest/gr/rande.html#ddb_region> e.g. `AWS_ENDPOINT_URL="https://dynamodb.eu-west-2.amazonaws.com"`

This still caused the same issue. To resolve this issue I unset the variable locally and removed it from Gitpod

```sh
gp env -u AWS_ENDPOINT_URL
unset AWS_ENDPOINT_URL
```

Once this had been unset I was able to run all aws_cli commands and run docker-compose

### Bootstrap Script

To automate tasks that would not run when the `.gitpod.yml` file did not work I created a [`./bin/bootstrap`](../bin/bootstrap) script. I also created a local version for my local environment [`./bin/bootstrap-local`](../bin/bootstrap-local.sh)

```sh
#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="bootstrap"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

ABS_PATH=$(readlink -f "$0")
BIN_DIR=$(dirname $ABS_PATH)

# Connect to ECR
source "$BIN_DIR/ecr/login"

# Configure Gitpod connectivity
source "$THEIA_WORKSPACE_ROOT/bin/rds/update-sg-rule"
source "$THEIA_WORKSPACE_ROOT/bin/ddb/update-sg-rule"

# Generate environment variables
ruby "$BIN_DIR/backend/generate-env"
ruby "$BIN_DIR/frontend/generate-env"

# Install CFN section
source "$BIN_DIR/cfn/initialise.sh"

# Install SAM section
source "$BIN_DIR/sam/initialise.sh"
```

### Warnings being shown when running static build

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/f48f2701-963e-4155-9e7c-e696f9a3931d)

These were addressed by commenting out the following import line

`import ReactDOM from 'react-dom';`

## Proof of working in Production

### Messaging to AltUser working in Prod

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/96c55733-1300-442e-9b5a-7aa997c4924b)

### Cruds work in Prod

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/4ccf0c1e-73b8-40c8-b0f9-ebebc0b4d1fd)

### Replies working in Prod

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/4a211bcc-0ca3-4054-80a1-7d519c108076)

### Profile Image successfully uploaded

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/15174507-c716-499f-ac1c-4b9b02a59292)

### Bio Changed

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/376f5521-100e-455c-b64c-29cd3d815ae2)
