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