# Week 6 — Deploying Containers

Andrews Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-6/journal/week6.md>

## Script to Connect to Task ID for Backend

```sh
#!/usr/bin/bash

export TASK_ID=$(aws ecs list-tasks --cluster cruddur --service-name backend-flask --query 'taskArns[*]' --output json | jq -r 'join(",")')

aws ecs execute-command  \
--region $AWS_DEFAULT_REGION \
--cluster cruddur \
--task $TASK_ID \
--container backend-flask \
--command "/bin/bash" \
--interactive
```

## Spend Issues

I have been using Gitpod because despite using a local environment a lot of the tools did not work as expected. I am using a Windows machine with WSL2 installed.

With my GitPod spending running to about £30 / month I chose to now focus on fixing any possible issues with the environment.

### Configuring WSL2 to work using Windows Credentials

I had an earlier version of Git Installed. This was not able to pass the required credentials to WSL2. This meant I would have to configure WSL2 with a separate key. I did not want to do this as GIT can use Windows Credentials.

To take advantage of this feature I upgraded my existing Git Installation using WinGet

```powershell
winget install --id Git.Git -e --source winget
```

I then configured WSL2 to point to my Windows credential store using the following command.

```sh
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

Reference: <https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git>

### AWS CLI not running session-manager

WSL2 could not run session-manager and gave the following error.

```sh
Error: Cannot perform an interactive login from a non TTY device
```

I installed the new version which resolved this issue.

## Migrate existing domain to Route 53

My existing domain is with ionos.co.uk, I have pointed the name servers to Route 53 however the change takes 48 hours.

Migration worked within ionos but domain was no longer pingable. Creating the aliases to the ALB's resolved this issue.

The application is now accessible via the domain name and the migration has been successful.

## Issue with Backend container continually starting

When refactoring the scripts I accidentally moved the healthcheck accidentally out of the directory. This caused the container to fail the health checks and continually restart it. It would run locally so I was confused. I resolved this issue by connecting to the container and verifying that the healthcheck script was missing. Once restored the issue was resolved.
