# Week 3 — Decentralized Authentication

Week 3 Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-3/journal/week3.md>

## Cognito Errors

Received the following error when trying to signup.

```sh
InvalidParameterException: Username cannot be of email format, since user pool is configured for email alias.
```

This was because I had left the following option checked.

> Allow users to sign in with a preferred user name

## Cognito User Pool Options

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
