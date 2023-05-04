# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

Andrews Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-9-again/journal/week9.md>

## Overview

The aim of this week was to automate the build pipeline using CodeBuild. Codebuild would be configured to detect any changes made in the prod branch of our repository.

## Builds failing when unable to download source

![image](https://user-images.githubusercontent.com/5746804/236071180-0da14f07-fedd-4399-93d2-2b18904e5301.png)

No logs were visible when source was failing

![image](https://user-images.githubusercontent.com/5746804/236071251-861d1137-01e9-44aa-8344-ed6b475eaa6c.png)

Troubleshooting showed what the issue was

![image](https://user-images.githubusercontent.com/5746804/236071319-2abd8992-af82-48ab-b78b-aa1d5a27190e.png)

Build failing with permissions errors

![image](https://user-images.githubusercontent.com/5746804/236071079-06f98421-d832-4dcd-b63d-fa64f2e715fd.png)

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

IAM Role required changing
![image](https://user-images.githubusercontent.com/5746804/236071699-b62e8877-0a6d-4d3b-b927-63aa1bcbce76.png)

Locate Role in IAM
![image](https://user-images.githubusercontent.com/5746804/236072805-f117310f-308c-4450-b62a-ee4708a37b1b.png)

Create Inline Policy
![image](https://user-images.githubusercontent.com/5746804/236072896-83db2bd8-7680-4a33-9c0c-a2c2c8d9afea.png)

JSON Policy to Add

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

Call Policy -> ECRPermissions

![image](https://user-images.githubusercontent.com/5746804/236073102-11fa5c24-f2ca-489e-af9e-e7122e804066.png)

Successful Run once permissions have been granted.

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
