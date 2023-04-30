# Week 8 — Serverless Image Processing

Andrew's Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-8-serverless-cdk/journal/week8.md>

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

Initially double clicking on this caused an error but I managed to resolve this by appending / at the beginning of the URL which I had missed out.

I also wrote this up in a Blog post to provide more detail.

<https://shehzadashiq.hashnode.dev/aws-cloud-project-bootcamp-dynamic-user-handles>

## Creating S3 Upload

npm i @aws-sdk/client-s3 --save

<https://github.com/aws/aws-sdk-js-v3#getting-started>
