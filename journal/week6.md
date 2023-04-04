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

## Migrate existing domain to Route 53

My existing domain is with ionos.co.uk, I have pointed the name servers to Route 53 however the change takes 48 hours.

