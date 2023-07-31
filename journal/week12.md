# Week 12 — Modern APIs

- [Week 12 — Modern APIs](#week-12--modern-apis)
  - [AppSync](#appsync)
    - [References](#references)
    - [App Sync Configuration](#app-sync-configuration)
    - [Click Create API](#click-create-api)
    - [Choose Import from DynamoDB](#choose-import-from-dynamodb)
    - [Specify API details](#specify-api-details)
    - [Specify GraphQL resources](#specify-graphql-resources)
    - [Review and create](#review-and-create)
    - [AppSync Settings Overview](#appsync-settings-overview)
    - [AppSync Schema](#appsync-schema)
    - [AppSync Data Source](#appsync-data-source)
    - [AppSync Query Tool](#appsync-query-tool)
    - [Structure of results returned by query](#structure-of-results-returned-by-query)
    - [Proof that AppSync works from the command line](#proof-that-appsync-works-from-the-command-line)
    - [Tables shown in DynamoDB To Show that AppSync has created an additional table](#tables-shown-in-dynamodb-to-show-that-appsync-has-created-an-additional-table)
    - [Error shown when trying to list message groups via AppSync](#error-shown-when-trying-to-list-message-groups-via-appsync)
  - [AppSync Frontend](#appsync-frontend)
  - [Using Recokgnition to moderate images](#using-recokgnition-to-moderate-images)
  - [CFN ModerationUser Stack](#cfn-moderationuser-stack)
    - [Create ModerationUser Template](#create-moderationuser-template)
    - [Create ModerationUser Deploy Script](#create-moderationuser-deploy-script)

## AppSync

<https://eu-west-2.console.aws.amazon.com/appsync/home?region=eu-west-2#/c2zdhezrnfh55dyaepvcpppofi/v1/home>

AppSync can be used as a bridge between DynamoDB and GraphQL. You use it as a intermediary and is part of AWS's Serverless component.

It took me a lot of time to figure out how DynamoDB worked. Queries in AppSync are referred to as Mutation. Even though initial configuration can be done via a wizard but a lot of configuration is required to implement this.

AppSync documentation for Python is lacking yet once you grasp the concepts it can be implemented.

I configured APPSYNC to work using IAM credentials. This means a `APPSYNC_ENDPOINT` variable needed to be created which pointed towards the `GraphQL endpoint` e.g. `APPSYNC_ENDPOINT="<https://dz6ahgar65hf3gx4pzddkvy2mi.appsync-api.eu-west-2.amazonaws.com/graphql>"`

I was able to get a list of message groups and messages via the command line however I could not get this working via the GUI so unfortunately had to revert it. I include proof that I was able to communicate with AppSync using the command line.

I would have liked to have had some more time to be able to fully implement the features implemented via DynamoDB so that AppSync could fully replace it. This however requires more research and understanding of key concepts for DynamoDB.

The code was implemented as a library function titled `AppSync` its [code](../backend-flask/lib/appsync.py) is here and has only two functions implemented. To test the functionality the following two lines need to be uncommented.

```py
# AppSync.list_message_groups(appsync,"4fa2d4e6-11f3-4b39-9ec8-a421d4faaa0a")
# AppSync.list_messages(appsync,"dba1f675-4793-4ad8-aa25-29c37b9eada6")
```

I am sure if I had more time to troubleshoot I would have been able to resolve this issue.

### References

- (Sample Code I utilised)<https://gist.github.com/angysmark/d6fbec3ad559c442d02dd23e1c14d586#file-appsync_client-py>
- <https://levelup.gitconnected.com/connect-to-aws-appsync-using-python-heres-how-806c702e0e18>
- <https://stackoverflow.com/questions/60293311/how-to-send-a-graphql-query-to-appsync-from-python>
- <https://docs.aws.amazon.com/appsync/latest/devguide/tutorial-dynamodb-resolvers.html#setting-up-the-addpost-resolver-dynamodb-putitem>
- <https://aws.amazon.com/graphql/graphql-dynamodb-data-modeling/>
- <https://css-tricks.com/how-to-make-graphql-and-dynamodb-play-nicely-together/>
- <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html>

### App Sync Configuration

Navigate to AppSync

### Click Create API

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/4db768a1-5d44-44b5-9429-141128cbe977)

### Choose Import from DynamoDB

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/1a89bbd2-fffc-42cb-af6d-6242be7ae32a)

| Option | Value |
| ----------- | ----------- |
|API Name|crudAppSyncApi|
|DynamoDB table region|Your-Region|
|DynamoDB table name|ShouldPickUpYourDb|
|Service role|Create and use a new service role|

### Specify API details

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/451c2e48-d602-483d-a679-dc279e3c30c1)

### Specify GraphQL resources

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/87cbdd57-5623-4a18-8f04-4e2f1f724ded)

### Review and create

Initial version which missed out most fields

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/0071aad8-1d4a-4304-9567-41f59bb9d94e)

Updated to include all necessary fields

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/6fdffbbd-6e44-4353-ad14-56c7bd6a43b3)

Click `Create API`

### AppSync Settings Overview

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/a8616985-f009-4d79-bd5a-1614688b2fc4)

### AppSync Schema

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/1be2bb37-4b7b-4321-9e05-dd0cdc96a4ba)

### AppSync Data Source

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/571731dc-2ac0-44d8-9a3a-d0155ca9ff77)

### AppSync Query Tool

This tool was invaluable in testing GraphQL queries to understand how a query should be constructed. In this screenshot the authorisation shows that the authentication method is `API Key`. It needs to be configured this way as the tool does not support IAM authentication. Make note to change this as required when testing.

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/3ce77644-c987-4ed2-944d-00a9b688b819)

### Structure of results returned by query

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/001f65b0-badc-4b9f-adc5-7e3745bf5a03)

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/13e3ab84-43fc-49c3-b595-0582c8700b7a)

### Proof that AppSync works from the command line

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/1fc4e3e1-bcad-4a78-9d18-ca2849bcac82)

### Tables shown in DynamoDB To Show that AppSync has created an additional table

![image](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/assets/5746804/f05c466d-d587-452e-934d-837ba938cc74)

### Error shown when trying to list message groups via AppSync

```sh
192.168.138.9 - - [31/Jul/2023 04:20:19] "GET /api/message_groups HTTP/1.1" 500 -
192.168.138.9 - - [31/Jul/2023 04:20:40] "OPTIONS /api/message_groups HTTP/1.1" 200 -
[2023-07-31 04:20:40,171] ERROR in app: Exception on /api/message_groups [GET]
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/usr/local/lib/python3.10/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
  File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "/usr/local/lib/python3.10/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/backend-flask/lib/cognito_jwt_token.py", line 142, in decorated_function
    return f(*args, **kwargs)
  File "/backend-flask/routes/messages.py", line 21, in data_message_groups
    model = MessageGroups.run(cognito_user_id=g.cognito_user_id)
  File "/backend-flask/services/message_groups.py", line 36, in run
    data = AppSync.list_message_groups(appsync,my_user_uuid)
  File "/backend-flask/lib/appsync.py", line 119, in list_message_groups
  File "/usr/local/lib/python3.10/site-packages/gql/client.py", line 403, in execute
    return self.execute_sync(
  File "/usr/local/lib/python3.10/site-packages/gql/client.py", line 220, in execute_sync
    with self as session:
  File "/usr/local/lib/python3.10/site-packages/gql/client.py", line 702, in __enter__
    return self.connect_sync()
  File "/usr/local/lib/python3.10/site-packages/gql/client.py", line 686, in connect_sync
    self.session.fetch_schema()
  File "/usr/local/lib/python3.10/site-packages/gql/client.py", line 881, in fetch_schema
    execution_result = self.transport.execute(parse(get_introspection_query()))
  File "/usr/local/lib/python3.10/site-packages/gql/transport/requests.py", line 220, in execute
    response = self.session.request(
  File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 575, in request
    prep = self.prepare_request(req)
  File "/usr/local/lib/python3.10/site-packages/requests/sessions.py", line 486, in prepare_request
    p.prepare(
  File "/usr/local/lib/python3.10/site-packages/requests/models.py", line 368, in prepare
    self.prepare_url(url, params)
  File "/usr/local/lib/python3.10/site-packages/requests/models.py", line 439, in prepare_url
    raise MissingSchema(
requests.exceptions.MissingSchema: Invalid URL 'None': No scheme supplied. Perhaps you meant https://None?
192.168.138.9 - - [31/Jul/2023 04:20:40] "GET /api/message_groups HTTP/1.1" 500 -
```

## AppSync Frontend

Initially I was aiming to integrate it into React but later realised it was a more natural fit in the backend. This is here just for reference and was not fully implemented

```sh
cd frontend-react-js
npm install -g @aws-amplify/cli
amplify add codegen --apiId c2zdhezrnfh55dyaepvcpppofi
```

- Choose `Choose the code generation language target javascript`
- Choose `Enter the file name pattern of graphql queries, mutations and subscriptions (src/graphql/**/*.js)`
- Choose `Do you want to generate/update all possible GraphQL operations - queries, mutations and subscriptions Yes`
- Choose `Enter maximum statement depth [increase from default if your schema is deeply nested] (2)`

Code

```sh
gitpod /workspace/aws-bootcamp-cruddur-2023/frontend-react-js (appSync) $ amplify init
Note: It is recommended to run this command from the root of your app directory
? Enter a name for the project crudAppSync
The following configuration will be applied:

Project information
| Name: crudAppSync
| Environment: dev
| Default editor: Visual Studio Code
| App type: javascript
| Javascript framework: react
| Source Directory Path: src
| Distribution Directory Path: build
| Build Command: npm run-script build
| Start Command: npm run-script start

? Initialize the project with the above configuration? Yes
Using default provider  awscloudformation
? Select the authentication method you want to use: AWS access keys
? accessKeyId:  ********************
? secretAccessKey:  ****************************************
? region:  eu-west-2
Adding backend environment dev to AWS Amplify app: d1vh0giv5pijbv

Deployment completed.
Deploying root stack crudAppSync [ ---------------------------------------- ] 0/4
        amplify-crudappsync-dev-214431 AWS::CloudFormation::Stack     CREATE_IN_PROGRESS             Thu Jul 27 2023 21:44:32…     
        UnauthRole                     AWS::IAM::Role                 CREATE_IN_PROGRESS             Thu Jul 27 2023 21:44:35…     
        AuthRole                       AWS::IAM::Role                 CREATE_IN_PROGRESS             Thu Jul 27 2023 21:44:35…     
        DeploymentBucket               AWS::S3::Bucket                CREATE_IN_PROGRESS             Thu Jul 27 2023 21:44:35…     

✔ Help improve Amplify CLI by sharing non sensitive configurations on failures (y/N) · yes
Deployment state saved successfully.
✔ Initialized provider successfully.
✅ Initialized your environment successfully.

Your project has been successfully initialized and connected to the cloud!

Some next steps:
"amplify status" will show you what you've added already and if it's locally configured or deployed
"amplify add <category>" will allow you to add features like user login or a backend API
"amplify push" will build all your local backend resources and provision it in the cloud
"amplify console" to open the Amplify Console and view your project status
"amplify publish" will build all your local backend and frontend resources (if you have hosting category added) and provision it in the cloud

Pro tip:
Try "amplify add api" to create a backend API and then "amplify push" to deploy everything
```

## Using Recokgnition to moderate images

- Create User to use with lambda
- Create ModerationUser Stack

I was aiming to use this to moderate images however as I was also looking at implementing AppSync I had to focus on that instead due to lack of time. My idea of implementation was to create a SNS notification on the avatar upload bucket.

Once an image had been implemented it would be checked for suitability. If unsuitable it would have been replaced with a stock image.

Another option I had been exploring was using step lambdas.

`The steps here are incomplete and more of an illustration of how I had thought that this feature would be implemented`

## CFN ModerationUser Stack

### Create ModerationUser Template

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  aws/cfn/moderation-user
cd aws/cfn/moderation-user
touch template.yaml config.toml
```

Update config.toml with the following changing `bucket` and `region` as appropriate

```config
[deploy]
bucket = 'cfn-tajarba-artifacts'
region = 'eu-west-2'
stack_name = 'CrdModerationUser'
```

The user requires the following permissions, `AmazonRekognitionFullAccess` and `AmazonS3ReadOnlyAccess`. To simplify this I decided to create the user via CloudFormation and merge both permissions into a policy I called `ModerationFullAccessPolicy`.

Update `aws/cfn/moderation-user/template.yaml` with the following code.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  CruddurModerationUser:
    Type: "AWS::IAM::User"
    Properties:
      UserName: "cruddur_moderation_user"
  ModerationFullAccessPolicy:
    Type: "AWS::IAM::Policy"
    Properties:
      PolicyName: "ModerationFullAccessPolicy"
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Action:
              - "s3:Get*"
              - "s3:List*"
              - "s3-object-lambda:Get*"
              - "s3-object-lambda:List*"
              - "rekognition:*"
            Resource: "*"
      Users:
        - !Ref CruddurModerationUser
```

### Create ModerationUser Deploy Script

With all the pre-requisites in place the service stack can now be created.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir -p  bin/cfn
cd bin/cfn
touch moderation-deploy
chmod u+x moderation-deploy
```

I modified the script to not have hardcoded values as I am using my local machine and GitPod for development.

```sh
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="CFN_MODERATIONUSER_DEPLOY"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

# Get the absolute path of this script
ABS_PATH=$(readlink -f "$0")
CFN_BIN_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $CFN_BIN_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
CFN_PATH="$PROJECT_PATH/aws/cfn/moderation-user/template.yaml"
CONFIG_PATH="$PROJECT_PATH/aws/cfn/moderation-user/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix db \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-moderation-user \
  --capabilities CAPABILITY_NAMED_IAM
```

```yaml
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"
            ],
            "Resource": "*"
        }
    ]
}
```

```yaml
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:*"
            ],
            "Resource": "*"
        }
    ]
}
```

```yaml
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*",
                "rekognition:*"
            ],
            "Resource": "*"
        }
    ]
}
```
