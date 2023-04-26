# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

Andrews Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-9-again/journal/week9.md>

Empty So Far

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

## Issue when trying to compose backend container in new Workspace

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
      got_request_exception.connect(rollbar.contrib.flask.report_exception, app)\
```

The container now builds successfully.
