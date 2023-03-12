# Week 4 — Postgres and RDS

Andrew Notes: <https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-4/journal/week4.md>

CDE Troubleshooting: <https://www.linuxtek.ca/2023/03/10/aws-cloud-project-bootcamp-solving-the-cde-problem/>

Manage master credentials in AWS Secrets Manager is convenient to use.

Had a problem with the db-schema-load script. I had the following

```sh
$echo $schema_path
```

instead of

```sh
echo $schema_path
```

This gave me errors when trying to output the path. I thought there was something wrong with my environment instead of a typo.

## Configured local VSCode environment automatically using Tasks

I wanted an equivalent locally of the way gitpod.yml was able to configure the workspace automatically. Researching the issue pointed me towards tasks. I created a folder called .vscode and within it created a file tasks.json.

The tasks.json file holds all tasks for the local workspace.

I wanted to create a task that would automatically install the npm packages in the frontend-react-js folder

```sh
npm i
```

I modified an automatically generated task from vscode to the below. This snippet will run whenever the folder is opened. Its working path is frontend-react-js and the windows will always be displayed so we can tell that the task has run.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "npm",
            "script": "install",
            "path": "frontend-react-js",
            "group": "build",
            "problemMatcher": [],
            "label": "npm: install - frontend-react-js",
            "detail": "install dependencies from package",
            "presentation": {
                                "reveal": "always",
                                "group": "develop",
                                "panel": "new"
                         },
                "runOptions": {
                                "runOn": "folderOpen"
                        }
        }
        ]
}
```

Successful output once a task has been run.

![Task Run Successfully](https://user-images.githubusercontent.com/5746804/224539915-76efbebe-b8bf-4451-8cec-c3b151ae0e51.png)
