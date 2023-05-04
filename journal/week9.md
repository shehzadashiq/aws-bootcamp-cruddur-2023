# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

Andrews Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-9-again/journal/week9.md>

## Overview

### Videos for week 9

- Week 9 Livestream <https://www.youtube.com/watch?v=DLYfI0ehMZE>
- Fix CodeBuild Issues <https://www.youtube.com/watch?v=py2E1f0IZg0>
- CodePipeline <https://www.youtube.com/watch?v=EAudiRT9Alw&ab_channel=ExamPro>

The aim of this week was to automate the build pipeline using CodeBuild and CodePipeline. This would provide us with a complete CI/CD pipeline [Further Reading](https://aws.amazon.com/blogs/devops/complete-ci-cd-with-aws-codecommit-aws-codebuild-aws-codedeploy-and-aws-codepipeline/)

**Integration**
Codebuild would be configured to detect any changes made in the prod branch of our repository.

**Deployment**
CodePipeline would then deploy the changes automatically.

## Pre-Requisites

- Buildspec.yml - This needs to be created in backend-flask i.e `backend-flask/buildspec.yml` [buildspec.yml](<https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/backend-flask/buildspec.yml>)
- Policy for permissions required for codebuild to run successfully [policy-file](<https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/policies/ecr-codebuild-backend-role.json>)
- Prod branch in repository. Any Pull requests will be detected by CodeBuild

## Troubleshooting

### Builds failing when unable to download source

### Builds would timeout and not proceed. An earlier build which I deleted kept running for 45 minutes without progressing

![image](https://user-images.githubusercontent.com/5746804/236071180-0da14f07-fedd-4399-93d2-2b18904e5301.png)

### No logs were visible when source was failing

![image](https://user-images.githubusercontent.com/5746804/236071251-861d1137-01e9-44aa-8344-ed6b475eaa6c.png)

### Troubleshooting showed builds were hanging at downloading source

![image](https://user-images.githubusercontent.com/5746804/236071319-2abd8992-af82-48ab-b78b-aa1d5a27190e.png)

### Misconfigured Environment

![image](https://user-images.githubusercontent.com/5746804/236330170-da0cecfd-de54-4888-9c6b-6617a6a2c50a.png)

Investigation showed that the environment had been misconfigured.

- VPC had been configured, this was not needed
- Security Groups had been configured
- Environment variables had been configured in the CodeBuild project. Andrew had configured this in his buildspec.yml however configuring it in the project had the same issue and was the main reason for why the builds had been failing without logs.

### Builds failing with permissions errors

Despite resolving this issue builds still failed. Logs showed the codebuild role was not authorised to perform various tasks required to build successfully.

![image](https://user-images.githubusercontent.com/5746804/236071079-06f98421-d832-4dcd-b63d-fa64f2e715fd.png)

### Text from log files

```sh
20 | [Container] 2023/05/03 23:07:48 Phase complete: DOWNLOAD_SOURCE State: SUCCEEDED
-- | --
21 | [Container] 2023/05/03 23:07:48 Phase context status code:  Message:
22 | [Container] 2023/05/03 23:07:48 Entering phase INSTALL
23 | [Container] 2023/05/03 23:07:48 Running command echo "cd into $CODEBUILD_SRC_DIR/backend"
24 | cd into /codebuild/output/src377814590/src/github.com/shehzadashiq/aws-bootcamp-cruddur-2023/backend
25 |  
26 | [Container] 2023/05/03 23:07:48 Running command cd $CODEBUILD_SRC_DIR/backend-flask
27 |  
28 | [Container] 2023/05/03 23:07:48 Running command aws ecr get-login-password --region $AWS_DEFAULT_REGION \| docker login --username AWS --password-stdin $IMAGE_URL
29 |  
30 | An error occurred (AccessDeniedException) when calling the GetAuthorizationToken operation: User: arn:aws:sts::797130574998:assumed-role/codebuild-cruddur--service-role/AWSCodeBuild-b0931d7a-83c6-4df9-a555-f341715bf817 is not authorized to perform: ecr:GetAuthorizationToken on resource: * because no identity-based policy allows the ecr:GetAuthorizationToken action
31 | Error: Cannot perform an interactive login from a non TTY device
32 |  
33 | [Container] 2023/05/03 23:08:01 Command did not exit successfully aws ecr get-login-password --region $AWS_DEFAULT_REGION \| docker login --username AWS --password-stdin $IMAGE_URL exit status 1
34 | [Container] 2023/05/03 23:08:01 Phase complete: INSTALL State: FAILED
35 | [Container] 2023/05/03 23:08:01 Phase context status code: COMMAND_EXECUTION_ERROR Message: Error while executing command: aws ecr get-login-password --region $AWS_DEFAULT_REGION \| docker login --username AWS --password-stdin $IMAGE_URL. Reason: exit status 1
```

### IAM Role required changing

The codebuild role needed to be amended

![image](https://user-images.githubusercontent.com/5746804/236071699-b62e8877-0a6d-4d3b-b927-63aa1bcbce76.png)

### Locate Role in IAM

![image](https://user-images.githubusercontent.com/5746804/236072805-f117310f-308c-4450-b62a-ee4708a37b1b.png)

### Create Inline Policy

![image](https://user-images.githubusercontent.com/5746804/236072896-83db2bd8-7680-4a33-9c0c-a2c2c8d9afea.png)

### JSON Policy to Add

The following permissions need to be applied to the role [policy-file](<https://github.com/shehzadashiq/aws-bootcamp-cruddur-2023/blob/main/aws/policies/ecr-codebuild-backend-role.json>)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:GetAuthorizationToken",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": "*"
    }
  ]
}
```

### Name Policy to ECRPermissions

![image](https://user-images.githubusercontent.com/5746804/236073102-11fa5c24-f2ca-489e-af9e-e7122e804066.png)

### Builds run successfully once permissions have been granted

![image](https://user-images.githubusercontent.com/5746804/236074562-e6aee963-b88e-4c83-8cc7-31573ec7968b.png)

## Issue when trying to compose backend container in new Workspace

This is unrelated to the work required this week but what I noticed when I tried to run my application in GitPod.

After migrating to a new workspace I encountered the following issue when building.

![image](https://user-images.githubusercontent.com/5746804/234458289-3396b9ba-9371-4e13-a4a9-628a7a2f68e0.png)

```sh
aws-bootcamp-cruddur-2023-backend-flask-1      |     __import__(module_name)
aws-bootcamp-cruddur-2023-backend-flask-1      |   File "/backend-flask/app.py", line 112, in <module>
aws-bootcamp-cruddur-2023-backend-flask-1      |     @app.before_first_request
aws-bootcamp-cruddur-2023-backend-flask-1      | AttributeError: 'Flask' object has no attribute 'before_first_request'. Did you mean: '_got_first_request'
```

According to this article: <https://stackoverflow.com/questions/73570041/flask-deprecated-before-first-request-how-to-update/74629704#74629704>

`before_first_request is deprecated and will be removed from Flask 2.3`

To resolve this I had to do the following

```py
# @app.before_first_request
with app.app_context():
  def init_rollbar():
      """init rollbar module"""
      rollbar.init(
          # access token
          rollbar_access_token,
          # environment name
          'production',
          # server root directory, makes tracebacks prettier
          root=os.path.dirname(os.path.realpath(__file__)),
          # flask already sets up logging
          allow_logging_basic_config=False)

      # send exceptions from `app` to rollbar, using flask's signal system.
      got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
```

The container now builds successfully.
