# Week 8 — Serverless Image Processing

- [Overview](#overview)
- [Pre-Requisites](#pre-requisites)
- [Journal Summary](#journal-summary)

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

- The following npm packages installed globally ([aws-cdk](https://www.npmjs.com/package/aws-cdk), [aws-cdk-lib](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html))
- The following npm packages installed for our lambda ([sharp](https://www.npmjs.com/package/sharp), [@aws-sdk/client-s3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/))
- S3 Bucket which we will upload our images to assets

---

## CDK Pipeline Creation

### Folder for Pipeline

We will store our Pipeline in a folder called `thumbing-serverless-cdk` in the root of our repository.

```sh
cd /workspace/aws-bootcamp-cruddur-2023
mkdir thumbing-serverless-cdk
```

### S3 Bucket for images

`assets.<domain_name>`

### Sharp Installation script

Sharp Documentation: <https://sharp.pixelplumbing.com/install>

```sh
npm install
rm -rf node_modules/sharp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux --libc=glibc sharp
```

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

## Creating S3 Upload

npm i @aws-sdk/client-s3 --save

<https://github.com/aws/aws-sdk-js-v3#getting-started>

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

npm install aws-jwt-verify --save

## S3 Bucket Issue

Created the bucket according to Andrew's directions. Items in the avatar folder were visible however items in the banners folder were not.

Trying to solve this by creating another bucket and troubleshooting this

This did not resolve the issue so I have placed the banner in the avatars directory. Not the ideal solution but I need a workaround for now.

In this instance we can see that the Avatar image is displaying fine

![image](https://user-images.githubusercontent.com/5746804/234272652-f5698bfb-16ca-482b-9fc6-4ef565e713e8.png)

Banner image placed in the banner folder does not display only a 1x1 pixel is displayed.

![image](https://user-images.githubusercontent.com/5746804/234272936-d99df89e-366d-4648-8258-c1b9b31ecb3f.png)

Verified that the banner.jpg exists in S3 bucket

![image](https://user-images.githubusercontent.com/5746804/234273214-9a8d032c-d375-45c6-aed5-8de2551da96c.png)

Verified that all images exist in avatars folder

![image](https://user-images.githubusercontent.com/5746804/234273396-7ae0437b-afc5-41fb-b6b6-61fcd4adc722.png)

The same image uploaded to the avatars folder displays without any issue.

![image](https://user-images.githubusercontent.com/5746804/234273571-9b150301-ca9a-4201-b86e-ae70003a035f.png)

This has had me scratching my head for days but I could not resolve it. I created another bucket and cloudfront distribution too however the cloudfront distribution could not resolve the domain name so I abandoned testing it with that approach.

![image](https://user-images.githubusercontent.com/5746804/234274388-9cc2672f-6758-47d6-9ea1-5d5001804439.png)

I opened a ticket and one of the other bootcampers mentioned that this might be a problem with Ad-Blockers. It turns out that Kaspersky was treating the image as a banner and hiding it. To counteract this I have created a new folder called images and placed the banner in it.

Setting in Kaspersky that caused the issue.

![image](https://user-images.githubusercontent.com/5746804/234359114-132d52c9-bbdc-4457-9a33-3f005a953f35.png)

## CORS Not Working

Following the videos and looking through the discord, I cannot get CORS working.

Currently I have had to disable the CruddurApiGatewayLambdaAuthoriser completely :(

I aim to continue with week 9 and then come back to troubleshoot this issue as currently it has put everything I am doing on hold.

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
This however was not the issue. The fault was that I had misconfigured the source path. The lambda was looking at ```sh avatar/original``` while the image was being uploaded to ```sh avatars/original```.

3. The initial issue was Kaspersky blocking all banners on the website. One of the boot campers pointed this out to me. To overcome this I had to place the banner in another folder in my s3 bucket and ensure the file was not named banner.jpg

4. CORS issues which were due to misconfiguration of the following

- I had kept copy pasting the URL of the workspace and missed out the port number of the frontend for "Access-Control-Allow-Origin" in
cruddur-upload-avatar/function.rb
- I had attached an authorisation to the OPTIONS route in the API gateway. This resulted in a 401 error
- In cruddur-upload-avatar/function.rb I had a put at the end of the function for debugging. Andrew explained that this would result in the pre-signed URL not being returned

Once these issues were fixed I was able to successfully upload the image based on the currently logged in users id.
