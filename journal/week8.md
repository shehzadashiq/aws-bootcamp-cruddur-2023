# Week 8 — Serverless Image Processing

- [Overview](#overview)
- [Pre-Requisites](#pre-requisites)
- [CDK Pipeline Creation](#cdk-pipeline-creation)
- [Create CloudFront Distribution](#create-cloudfront-distribution)
- [Avatar Upload Implementation](#avatar-upload-implementation)
- [Issue when creating Serverless Image Process](#issue-when-creating-serverless-image-process)
- [Dynamically passing user handle to profile](#dynamically-passing-user-handle-to-profile)
- [Ruby Initialisation for Application](#ruby-initialisation-for-application)
- [Code to dynamically get the GitPod name in Ruby](#code-to-dynamically-get-the-gitpod-name-in-ruby)
- [Repo for JWT Token](#repo-for-jwt-token)
- [S3 Bucket Issue](#s3-bucket-issue)
- [Journal Summary](#journal-summary)

---

## Overview

### Videos for week 8

- [Week 8 Livestream](https://www.youtube.com/watch?v=YiSNlK4bk90)
- [Serverless Image Process CDK](https://www.youtube.com/watch?v=jyUpZP2knBI)
- [Serving Avatars via CloudFront](https://www.youtube.com/watch?v=Hl5XVb7dL6I)
- [Implement Users Profile Page](https://www.youtube.com/watch?v=WdVPx-LLjQ8)
- [Implement Migrations Backend Endpoint and Profile Form](https://www.youtube.com/watch?v=PTafksks528)
- [Implement Avatar Uploading (Part 1)](https://www.youtube.com/watch?v=Bk2tq4pliy8)
- [Fix CORS for API Gateway](https://www.youtube.com/watch?v=eO7bw6_nOIc)
- [Fix CORS Final AWS Lambda Layers](https://www.youtube.com/watch?v=uWhdz5unipA)
- [Render Avatar from CloudFront](https://www.youtube.com/watch?v=xrFo3QLoBp8)

[Andrew's Notes](https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-8-serverless-cdk/journal/week8.md)

The aim of this week is to allow users to upload their own profile images via Serverless Image Process. To do so we use the [CDK - Cloud Development Kit](https://aws.amazon.com/cdk/) to create a [CDK Pipeline](https://docs.aws.amazon.com/cdk/v2/guide/cdk_pipeline.html).

CDK Pipelines can automatically build, test, and deploy new versions of our pipeline. CDK Pipelines are self-updating. Once we add application stages or stacks, the pipeline automatically reconfigures itself to deploy them.

We will use the CDK pipeline implemented in JavaScript that will perform the following tasks for us.

- Use the sharp package to process an uploaded image and resize it to create a thumbnail
- Write an AWS Lambda function
- Deploy our Lambda function
- Import an existing S3 bucket that contains the source image
- Create an S3 bucket that will be used to process the uploaded image
- Create a SNS (Simple Notification Service) to process on the PUT function and invoke our Lambda function

To invoke the lambda the following changes need to be made to the application

- Implement a file upload function in the frontend
- Our PostGres database needs to be updated to include a biography field
- Update SQL scripts to retrieve this information when matched to the users cognito ID

---

## Pre-Requisites

- The following npm packages installed globally ([aws-cdk](https://www.npmjs.com/package/aws-cdk), [aws-cdk-lib](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html), [dotenv](https://www.npmjs.com/package/dotenv))
- The following npm packages installed for our lambda ([sharp](https://www.npmjs.com/package/sharp), [@aws-sdk/client-s3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/))
- S3 Bucket which we will upload our images to assets with the name `assets.<domainname>`

---

## CDK Pipeline Creation

### Install Global Packages

Run the following command to install the required packages

```sh
npm i aws-cdk aws-cdk-lib dotenv -g
```

To automate the installation of these packages and our lambda package (explained in detail later) for our gitpod environment we can add a task by inserting the following section in our `.gitpod.yml`

```yml
  - name: cdk
    before: |
      npm install aws-cdk -g
      npm install aws-cdk-lib -g
      cd thumbing-serverless-cdk
      npm i      
      cp env.example .env
```

### Folder for Pipeline

We will store our Pipeline in a folder called `thumbing-serverless-cdk` in the root of our repository.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
```

### Initialise CDK Pipeline

Navigate to the `thumbing-serverless-cdk` folder and initialise it for typescript.

```sh
cdk init app --language typescript
```

### Prepare and define CDK Pipeline environment

- Created a S3 bucket named `assets.tajarba.com` in my AWS account. This will be used to store avatar images, banners for the website
- Create the following file `.env.example`. This will be used by the lamba application to define the source and output buckets
- Create lambda function that will be invoked by our CDK stack in `aws\lambdas\process-images`
- Add the following code in the `thumbing-serverless-cdk/lib`[thumbing-serverless-cdk-stack.ts](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/thumbing-serverless-cdk/lib/thumbing-serverless-cdk-stack.ts)

### Create Sample .env.example file

```sh
cd /workspace/aws-bootcamp-cruddur-2023/thumbing-serverless-cdk
touch .env.example
```

#### Sample .env.example file

[.env.example](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/thumbing-serverless-cdk/.env.example)

```env
ASSETS_BUCKET_NAME="assets.tajarba.com"
THUMBING_S3_FOLDER_INPUT=""
THUMBING_S3_FOLDER_OUTPUT="avatars"
THUMBING_WEBHOOK_URL="https://api.tajarba.com/webhooks/avatar"
THUMBING_TOPIC_NAME="cruddur-assets"
THUMBING_FUNCTION_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/lambdas/process-images"
UPLOADS_BUCKET_NAME="tajarba-uploaded-avatars"
```

#### S3 Bucket for images

`assets.<domain_name>` e.g. `assets.tajarba.com`

### Create Lambda Function

Create the application in `aws\lambdas\process-images`

```sh
cd /workspace/aws-bootcamp-cruddur-2023/
mkdir -p aws/lambdas/
cd aws/lambdas/process-images
touch index.js s3-image-processing.js test.js
npm init -y
npm install sharp @aws-sdk/client-s3 --save
```

The code for these files is located in [process-images](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/tree/main/aws/lambdas/process-images)

Optionally there is also an [example.json](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/lambdas/process-images/example.json) that can be used to test the application using AWS Lambdas test function.

[Further Reading on using the AWS SDK](https://github.com/aws/aws-sdk-js-v3#getting-started)

### Bootstrap environment

[Bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html) is the process of provisioning resources for the AWS CDK before you can deploy AWS CDK apps into an AWS environment. (An AWS environment is a combination of an AWS account and Region).

Bootstrap the application using the command. The command assumes that you have set the AWS_ACCOUNT_ID and AWS_DEFAULT_REGIONS correctly.

`cdk bootstrap "aws://$AWS_ACCOUNT_ID/$AWS_DEFAULT_REGION"`

### Synthesise Application

Once bootstrapped you can first generate a CloudFormation template for the application using

`cdk synth`

### Deploy Environment

Deploy the CDK using AWS CloudFormation

`cdk deploy`

To verify the application has been deployed successfully, run the following command.

`cdk ls`

### Sharp Installation script

To use the sharp package within a lambda function the `node_modules` directory of the deployment package must include binaries for the Linux x64 platform. Once the npm package has been installed we need to run the following npm command.

```sh
cd /workspace/aws-bootcamp-cruddur-2023/thumbing-serverless-cdk
npm install
rm -rf node_modules/sharp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux --libc=glibc sharp
```

This process has been automated in the following script. [sharp install script](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/bin/avatar/build)

[Sharp Documentation](https://sharp.pixelplumbing.com/install#aws-lambda)

### Test Deployed Lambda

- Run the `bin/avatar/upload` [script](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/bin/avatar/upload) that uploads a file `data.jpg` to the source directory that the lambda is looking at
- Verify that the image has been uploaded to the destination bucket and that it has been resized to 512x512

Verify Original Image was uploaded
![image](https://user-images.githubusercontent.com/5746804/236935062-b2709a07-e3b0-4586-8685-9aedc5dfbc19.png)

Check how it looks, it should be 1920x1080
![image](https://user-images.githubusercontent.com/5746804/236934366-95a06f11-e1bc-4646-b618-a991d712994a.png)

Confirm that the lambda has placed the file in the s3 bucket
![image](https://user-images.githubusercontent.com/5746804/236934761-a2819bf5-78dc-4063-9305-9d73322f982a.png)

Check that the processed image was resized to 512x512
![image](https://user-images.githubusercontent.com/5746804/236934541-f898d773-70a0-4842-b10a-e177fb452aa7.png)

---

## Create CloudFront Distribution

[CloudFront](https://aws.amazon.com/cloudfront/) is a CDN (Content Delivery Network) by AWS. We will use it to serve content from our buckets by responding to HTTPS requests. It also allows us granular control over how assets are displayed.

### CloudFront Pre-Requisites

- Domain name registered to the `<domainname>` you are using. I am using <https://www.tajarba.com> and have it registered with [IONOS](https://www.ionos.co.uk/)
- Domain's name servers registered with Route 53
- Certificate registered for `<domainname>` in the us-east-1 zone in addition to your local region

### Certificate Creation

- Go to `AWS Certificate Manager (ACM)`
- Click `Request Certificate`
- Select `Request a public certificate`
- In `Fully qualified domain name` enter `<domainname>` e.g. `tajarba.com`
- Select `Add Another Name to this certificated` and add `*.tajarba.com`
- Ensure `DNS validation - recommended` is selected
- Click `Request`

![image](https://user-images.githubusercontent.com/5746804/236962435-8415b1a2-cdf5-4d91-8f9c-ba0f4e3fd9d7.png)

### Cloudfront Distribution Creation

The below settings use `assets.tajarba.com` as its example. **Everything else can be left as default**

| Option | Value |
| ----------- | ----------- |
| Origin domain | **Choose Amazon S3 bucket** `assets.tajarba.com` |
| Name | Set Automatically when you select the S3 bucket |
| Origin access | **Select** Origin access control settings (recommended) |
| Origin access control | `assets.tajarba.com` |
| Create a control setting | Select and choose the following **Sign requests (recommended)**,**Origin type=S3** |
| Viewer protocol policy | Redirect HTTP to HTTPS |
| Cache policy and origin request policy (recommended) | **Selected** |
| Cache policy | CachingOptimized |
| Origin request policy | CORS-CustomOrigin |
| Response headers policy | SimpleCORS |
| Alternate domain name (CNAME) | `assets.tajarba.com` |
| Custom SSL certificate | Certificate created for `tajarba.com` |

Once the CloudFront distribution has been created, we need to copy it's bucket policy. To copy this go to `Origins`, select the origin `assets.tajarba.com` and click `Edit`. Scroll to `Bucket Policy` and click `Copy Policy`

![image](https://user-images.githubusercontent.com/5746804/236963604-7a338a22-554f-4e57-a962-5b61fb64639c.png)

This policy needs to be applied to the bucket `assets.tajarba.com` under `Permissions` -> `Bucket Policy`

![image](https://user-images.githubusercontent.com/5746804/236964625-2f31f9c4-d61b-4dd2-9dc8-cb7688d529b3.png)

### Route 53 Record Creation

- Go to `Route 53`
- Click `Create hosted zone`
- `Domain name` -> `tajarba.com`
- `Type` = `Public hosted zone`
- Click `Create Hosted Zone`

![image](https://user-images.githubusercontent.com/5746804/236965650-c70e23c0-d837-48e2-9035-28edbebb66b3.png)

### Enable Invalidation

When uploading a new version of an image until it expires it will keep displaying the old version of the file. To stop this from happening we need to enable [invalidation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)

- In `Cloudfront` select the cloudfront distribution
- Select `Invalidations`
- Add the pattern `/*` and click `Create Invalidation`
- It will take a minute or so for the change to take effect

![image](https://user-images.githubusercontent.com/5746804/236966825-c0ee0711-4077-4fb0-a929-85b4744dc6c4.png)

### DB Changes

To display Biographic information about the user we need to add a text column called BIO. Andrew implemented a migration script but I chose to just change my [schema.sql](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/schema.sql) and [seed.sql](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/seed.sql) for convenience.

#### Schema.sql

```sql
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text NOT NULL,
  handle text NOT NULL ,
  email text NOT NULL ,
  cognito_user_id text,
  bio text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

#### Seed.sql

```sql
INSERT INTO public.users (display_name, handle, email,bio,cognito_user_id)
VALUES
  ('Shehzad Ali', 'shehzad','shehzad@exampro.co','NothingSoFar','MOCK'),
  ('Andrew Bayko', 'bayko','bayko@exampro.co','NothingSoFar','MOCK'),
  ('Andrew Brown', 'andrewbrown','andrew@exampro.co','NothingSoFar','MOCK');
```

---

## Avatar Upload Implementation

To upload avatars we will utilise a API gateway that will call a lambda function `lambda-authorizer` which authenticates the current user. This then calls `cruddur-upload-avatar` which returns a pre-signed URL. This pre-signed URL allows access to Cruddur to upload to the S3 bucket.

### Pre-Requisites for Avatar Upload

- Create a lambda function to authorise the currently logged in user `aws/lambdas/lambda-authorizer`
- Create a lambda function to upload the image `aws/lambdas/cruddur-upload-avatar/`
- Create an API gateway which invokes the lambda functions

### Implement CruddurAvatarUpload

- Create the skeleton structure of the application

```sh
cd /workspace/aws-bootcamp-cruddur-2023/
mkdir -p aws/lambdas/cruddur-upload-avatar/
cd aws/lambdas/cruddur-upload-avatar/
touch function.rb
bundle init
```

- After running `bundle init` a `Gemfile` will have been created. Add the following packages to it ["aws-sdk-s3", "ox", "jwt"] by editing it as below

```ruby
# frozen_string_literal: true

source "https://rubygems.org"

# gem "rails"
gem "aws-sdk-s3"
gem "ox"
gem "jwt"
```

- Install the required packages `bundle install`
- Update `function.rb` with this code [function.rb](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/lambdas/cruddur-upload-avatar/function.rb)
- Update the `Access-Control-Allow-Origin` sections with the URL of the frontend application e.g. `"Access-Control-Allow-Origin": "https://3000-shehzadashi-awsbootcamp-sf7toclaf7t.ws-eu96b.gitpod.io"`
- Verify lambda function works `bundle exec ruby function.rb`. This should return a pre-signed URL

### Implement Lambda-Authoriser

- Create the skeleton structure of the application

```sh
cd /workspace/aws-bootcamp-cruddur-2023/
mkdir -p aws/lambdas/lambda-authorizer/
cd aws/lambdas/lambda-authorizer/
touch index.js
npm init -y
npm install aws-jwt-verify --save
```

- Update `index.js` with this code [index.js](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/lambdas/lambda-authorizer/index.js)
- Download the files in this folder to a zip file as shown below. This file will be uploaded later as a lambda. Downloading these files will ensure all the required packages are available to the lambda function

![image](https://user-images.githubusercontent.com/5746804/236979393-2400618d-c39b-4d77-a8ae-3935dc43749d.png)

### Create functions in AWS Lambda

#### CruddurAvatarUpload

- Create a Ruby Application named `CruddurAvatarUpload`
- Upload the code from [function.rb](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/lambdas/cruddur-upload-avatar/function.rb) ensuring it has the correct GitPod frontend URL set in `Access-Control-Allow-Origin`
- Set an environment variable `UPLOADS_BUCKET_NAME` with `tajarba-uploaded-avatars` the location where avatars are to be uploaded to
- Edit `runtime settings` to have the handler set as `function.handler`
- Modify the current permissions policy and attach a new inline policy `PresignedUrlAvatarPolicy` using this [S3 Policy](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/policies/s3-upload-avatar-presigned-url-policy.json)

![image](https://user-images.githubusercontent.com/5746804/236981542-657fb41e-3108-41bd-89c0-4f22981d03fb.png)

S3 Policy using our bucket name

```yml
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::tajarba-uploaded-avatars/*"
        }
    ]
  }
```

#### CruddurApiGatewayLambdaAuthorizer

- Create a Node.js Application named `CruddurApiGatewayLambdaAuthorizer`
- Upload the zip file of the code we created earlier. If packaged and uploaded correctly it should look like this

![image](https://user-images.githubusercontent.com/5746804/236982683-93bef8f6-e68b-42cf-8dde-e3e5ce65dc3f.png)

- Set the environment variables `USER_POOL_ID` and `CLIENT_ID` with your Cognito clients `USER_POOL_I` and `AWS_COGNITO_USER_POOL_CLIENT_ID` respectively

### Update S3 Bucket COR Policy

- Under the permissions for `tajarba-uploaded-avatars` edit `Cross-Origin resource sharing (CORS)` with this [S3 CORS Policy](https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/s3/cors.json)

### Create API Gateway

- In `API Gateway`, create a `HTTP API` with api.<domain_name> e.g. `api.tajarba.com`
- Creat the two routes below

| Option | Value |
| ----------- | ----------- |
| POST | /avatars/key_upload with authoriser `CruddurJWTAuthorizer` which invokes lambda `CruddurApiGatewayLambdaAuthorizer`, and with integration `CruddurAvatarUpload` |
| OPTIONS |/{proxy+} without authoriser, but with integration `CruddurAvatarUpload` |

#### Routes for API Gateway - Post

![image](https://user-images.githubusercontent.com/5746804/236985624-dc341462-8ef2-4941-98f9-cd0bbd9f622f.png)

#### Routes for API Gateway - Options

![image](https://user-images.githubusercontent.com/5746804/236986257-cd93f57f-6326-4d4c-a2f2-949d0d95c1a0.png)

#### Authorisation for API Gateway

![image](https://user-images.githubusercontent.com/5746804/236985696-89167d97-a31a-4592-80fe-fcffa68ac49e.png)

#### Integration for KeyUpload

![image](https://user-images.githubusercontent.com/5746804/236985823-754184ab-fbc1-4cbf-a4d6-b1d4df5a18ff.png)

#### Integration for Options

![image](https://user-images.githubusercontent.com/5746804/236985914-44cd32cc-0a4d-446f-aae8-67b4b72385e8.png)

#### Cors for API Gateway

There should be no CORS configuration

![image](https://user-images.githubusercontent.com/5746804/236986009-6b8cc05a-cbb2-46e8-9158-badab44dbc1e.png)

#### Triggers for CruddurAvatarUpload

![image](https://user-images.githubusercontent.com/5746804/236985487-018939ac-8717-4c79-b2dc-1e0107c34951.png)

---

## Issue when creating Serverless Image Process

When creating the lambda, I face a few errors. Because of costs I had been working off my local machine. This installed sharp but once the lambda had been uploaded it would complain that sharp was missing. I resolved this by switching over to Gitpod

Once this issue had been resolve the lambda would still not trigger. I checked that the code was correct by testing it against sample JSON. This passed so I looked into various aspects in the cloudformation stack. I looked at the roles in cloudformation and saw the following error.

![image](https://user-images.githubusercontent.com/5746804/232346131-f3a24fda-9819-48e7-92f2-e0760d7b9d19.png)

This however was a red herring and wasted time. The reason for the code not working was that there were typos in the .env file. The lambda was looking at

```sh
avatar/original
```

while the image was being uploaded to

```sh
avatars/original
```

Once this was resolved the lambda processed images successfully.

---

## Dynamically passing user handle to profile

This makes the Profile Icon handle dynamic by removing @andrewbrown as a hardcoded URL.

In DesktopNavigation.js the following is hardcoded

```sh
profileLink = <DesktopNavigationLink 
      url="/@andrewbrown" 
      name="Profile"
      handle="profile"
      active={props.active} />
```

During my video grading Andrew mentioned that since the user had been already passed we should be able to access the property of it. A bit of trial and error later the following code works.

```sh
profileLink = <DesktopNavigationLink 
      url={"/@" + props.user.handle}
      name="Profile"
      handle="profile"
      active={props.active} />
```

This shows the @bayko profile when logged in as Bayko

![image](https://user-images.githubusercontent.com/5746804/234735739-03bb7353-79a5-4474-a7cf-4a5346a3b753.png)

Initially double clicking on this caused an error as it kept appending the username to the end of the URL repeatedly. I managed to resolve this by appending / at the beginning of the URL which I had missed out initially.

I also wrote this up in a Blog post to provide more detail.

<https://shehzadashiq.hashnode.dev/aws-cloud-project-bootcamp-dynamic-user-handles>

## Ruby Initialisation for Application

To initialise ruby in a directory run the following command

```sh
bundle init
```

To install the packages in a ruby bundle run the following command

```sh
bundle install
```

UPLOADS_BUCKET_NAME needs to be configured as a GitPOD environment variable

```sh
gp env UPLOADS_BUCKET_NAME="tajarba-uploaded-avatars"
```

Test Ruby function by running

```sh
bundle exec ruby function.rb
```

## Code to dynamically get the GitPod name in Ruby

I had written this up purely as a test.

```rb
workspace_id = ENV['GITPOD_WORKSPACE_ID']
workspace_cluster_host = ENV['GITPOD_WORKSPACE_CLUSTER_HOST']

workspace_url = "https://#{workspace_id}.#{workspace_cluster_host}"

puts "Workspace URL: #{workspace_url}"
```

## Repo for JWT Token

Repo documenting usage of JWT Tokens <https://github.com/awslabs/aws-jwt-verify>

`npm install aws-jwt-verify --save`

## S3 Bucket Issue

Created the bucket according to Andrew's directions. Items in the avatar folder were visible however items in the banners folder were not.

Trying to solve this by creating another bucket and troubleshooting this

This did not resolve the issue so I have placed the banner in the avatars directory. Not the ideal solution but I need a workaround for now.

### In this instance we can see that the Avatar image is displaying fine

![image](https://user-images.githubusercontent.com/5746804/234272652-f5698bfb-16ca-482b-9fc6-4ef565e713e8.png)

### Banner image placed in the banner folder does not display only a 1x1 pixel is displayed

![image](https://user-images.githubusercontent.com/5746804/234272936-d99df89e-366d-4648-8258-c1b9b31ecb3f.png)

### Verified that the banner.jpg exists in S3 bucket

![image](https://user-images.githubusercontent.com/5746804/234273214-9a8d032c-d375-45c6-aed5-8de2551da96c.png)

### Verified that all images exist in avatars folder

![image](https://user-images.githubusercontent.com/5746804/234273396-7ae0437b-afc5-41fb-b6b6-61fcd4adc722.png)

### The same image uploaded to the avatars folder displays without any issue

![image](https://user-images.githubusercontent.com/5746804/234273571-9b150301-ca9a-4201-b86e-ae70003a035f.png)

This has had me scratching my head for days but I could not resolve it. I created another bucket and cloudfront distribution too however the cloudfront distribution could not resolve the domain name so I abandoned testing it with that approach.

![image](https://user-images.githubusercontent.com/5746804/234274388-9cc2672f-6758-47d6-9ea1-5d5001804439.png)

I opened a ticket and one of the other bootcampers mentioned that this might be a problem with Ad-Blockers. It turns out that Kaspersky was treating the image as a banner and hiding it. To counteract this I have created a new folder called images and placed the banner in it.

### Setting in Kaspersky that caused the issue

![image](https://user-images.githubusercontent.com/5746804/234359114-132d52c9-bbdc-4457-9a33-3f005a953f35.png)

## CORS Not Working

Following the videos and looking through the discord, I could get CORS working.

To get uploads working I had to disable the CruddurApiGatewayLambdaAuthoriser completely :(

I continued with week 9 and then come back to troubleshoot this issue as it had put me quite far behind in my work.

---

## Journal Summary

Completed all the homework.

Challenges.
I managed to remove the hard-coded user profile of andrewbrown and instead use dynamic profiles by changing the profileLink url to

```typescript
"url={"/@" + props.user.handle}"
```

### Issues

1. Working from my local environment despite following the instructions to install the sharp and without no errors the lambda would complain that sharp had not been installed. The same issue happened despite using WSL2 and a Linux VM. To resolve this I had to resort to using GitPod.

2. Lambda would not trigger complaining "Entity does not exist. One of the entities that you specified for the operation does not exist. The role with the name ThumbingServerlessCDKStack-ThumbLambdaServiceRole cannot be found".
This however was not the issue. The fault was that I had misconfigured the source path. The lambda was looking at `avatar/original` while the image was being uploaded to `avatars/original`.

3. The initial issue was Kaspersky blocking all banners on the website. One of the boot campers pointed this out to me. To overcome this I had to place the banner in another folder in my s3 bucket and ensure the file was not named banner.jpg

4. CORS issues which were due to misconfiguration of the following

- I had kept copy pasting the URL of the workspace and missed out the port number of the frontend for "Access-Control-Allow-Origin" in
cruddur-upload-avatar/function.rb
- I had attached an authorisation to the OPTIONS route in the API gateway. This resulted in a 401 error
- In cruddur-upload-avatar/function.rb I had a put at the end of the function for debugging. Andrew explained that this would result in the pre-signed URL not being returned

Once these issues were fixed I was able to successfully upload the image based on the currently logged in users id.
