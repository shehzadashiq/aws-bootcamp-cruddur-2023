#! /usr/bin/bash

echo "db-schema-load"

# echo $1

# $schema_path="$(realpath .)/db/schema.sql"
$schema_path="$(pwd)/db/schema.sql"
$echo $schema_path

# if ["$1" == "prod"]; then
#     echo "Running in production mode"
#     URL=$PROD_CONNECTION_URL
# else
#     URL=$CONNECTION_URL
# fi

# psql $URL cruddur < $schema_path

