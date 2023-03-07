# Week 3 — Decentralized Authentication

Week 3 Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-3/journal/week3.md>

## Cognito Errors

Received the following error when trying to signup.

```sh
InvalidParameterException: Username cannot be of email format, since user pool is configured for email alias.
```

This was because I had both username and email in the following option. Only email should have been checked,

> Cognito user pool sign-in options

## Cognito User Pool Creation Options

Everything else can be left as default.

| Option | Value |
| ----------- | ----------- |
| Provider types | Cognito user pool |
| Cognito user pool sign-in options | - Email |
| User name requirements | **Nothing Checked** |
| Password policy | Cognito Defaults |
| Multi-factor authentication | No MFA |
| User account recovery |Enable self-service account recovery ->  **Email Only**)|
| Self-service sign-up          |Enable self-registration|
|Attribute verification and user account confirmation| Allow Cognito to -> **Send email message**|
|Verifying attribute changes|Keep original attribute value active|
|Required attributes|name,preferred_username|
| Email |Send email with Cognito|
|User pool name|cruddur-user-pool|
| Hosted authentication pages | Uncheck **Use the Cognito Hosted UI** |
| App type | Public Client|
| App client name | cruddur |
| Client secret | Don't generate a client secret |

## Observations

My local development system is a lot less forgiving than Gitpod.

If the following function does not exist then React will not load locally displaying the following error.

```sh
setCognitoErrors("Email is invalid or cannot be found.")   
```

![React Error](https://user-images.githubusercontent.com/5746804/223359323-8841126f-8d08-4af0-b7bd-0158fb997efd.png)

To resolve this the function needs to be renamed to setErrors. The same issue does not occur on Gitpod.