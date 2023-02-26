# Week 1 — App Containerization

## References

URL of backend application: <http://127.0.0.1:4567/api/activities/home>
URL of frontend: <http://localhost:3000/>

OpenAPI Responses Specification: <https://spec.openapis.org/oas/v3.1.0#responses-object>

Ruby on Rail Services: <https://www.toptal.com/ruby-on-rails/rails-service-objects-tutorial>

Week 1 Notes: <https://github.com/spurin/aws-bootcamp-cruddur-2023/blob/week-1-spurin/journal/week1.md>

Good Article for Debugging Connection Refused: <https://pythonspeed.com/articles/docker-connection-refused/>

## Notes from Andrew

## VSCode Docker Extension

Docker for VSCode makes it easy to work with Docker

<https://code.visualstudio.com/docs/containers/overview>

> Gitpod is preinstalled with this extension

## Containerize Backend

### Add Dockerfile

Create a file here: `backend-flask/Dockerfile`

```dockerfile
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

### Set environmental variables

Linux/Mac

```sh
export FRONTEND_URL='*'
export BACKEND_URL='*'
```

Windows

```sh
set FRONTEND_URL='*'
set BACKEND_URL='*'
```

### Build Backend Container

```sh
docker build -t  backend-flask ./backend-flask
```

### Run Backend Container

Run

```sh
docker run --rm -p 4567:4567 -e FRONTEND_URL='*' -e BACKEND_URL='*' -it backend-flask
```

Run in background

```sh
docker container run --rm -p 4567:4567 -d backend-flask (Does not work causes the error, typescript error)

docker container run --rm -p 4567:4567 -e FRONTEND_URL='*' -e BACKEND_URL='*' -d backend-flask
```

Return the container id into an Env Vat

```sh
CONTAINER_ID=$(docker run --rm -p 4567:4567 -e FRONTEND_URL='*' -e BACKEND_URL='*' -d backend-flask)
```

> docker container run is idiomatic, docker run is legacy syntax but is commonly used.

### Get Container Images or Running Container Ids

```sh
docker ps
docker images
```

### Send Curl to Test Server

```sh
curl -X GET http://localhost:4567/api/activities/home -H "Accept: application/json" -H "Content-Type: application/json"
```

### Check Container Logs

```sh
docker logs $CONTAINER_ID -f
docker logs backend-flask -f
docker logs $CONTAINER_ID -f
```

### Debugging  adjacent containers with other containers

```sh
docker run --rm -it curlimages/curl '-X GET \"http://localhost:4567/api/activities/home\" -H \"Accept: application/json\" -H \"Content-Type: application/json\"'
```

busybosy is often used for debugging since it install a bunch of thing

```sh
docker run --rm -it busybosy
```

### Gain Access to a Container

```sh
docker exec -it $CONTAINER_ID /bin/bash
```

docker exec -it mycontainer sh

> You can just right click a container and see logs in VSCode with Docker extension

### Delete an Image

```sh
docker image rm backend-flask --force
```

> docker rmi backend-flask is the legacy syntax, you might see this is old docker tutorials and articles.
> There are some cases where you need to use the --force

### Overriding Ports

```sh
FLASK_ENV=production PORT=8080 docker run -p 4567:4567 -it backend-flask
```

> Look at Dockerfile to see how ${PORT} is interpolated

## Containerize Frontend

## Run NPM Install

We have to run NPM Install before building the container since it needs to copy the contents of node_modules

```sh
cd frontend-react-js
npm i
```

### Create Docker File

Create a file here: `frontend-react-js/Dockerfile`

```dockerfile
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

### Build Fronted Container

```sh
docker build -t frontend-react-js ./frontend-react-js
```

### Run Container -01

```sh
docker run -p 3000:3000 -d frontend-react-js
```

## Multiple Containers

### Create a docker-compose file

Create `docker-compose.yml` at the root of your project.

```yaml
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3001-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur
```

## Adding DynamoDB Local and Postgres

We are going to use Postgres and DynamoDB local in future labs
We can bring them in as containers and reference them externally

Lets integrate the following into our existing docker compose file:

### Postgres

```yaml
services:
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
volumes:
  db:
    driver: local
```

### DynamoDB Local

```yaml
services:
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```

## Volumes

directory volume mapping

```yaml
volumes: 
- "./docker/dynamodb:/home/dynamodblocal/data"
```

named volume mapping

```yaml
volumes: 
  - db:/var/lib/postgresql/data

volumes:
  db:
    driver: local
```
