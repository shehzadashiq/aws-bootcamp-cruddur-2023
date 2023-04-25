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
