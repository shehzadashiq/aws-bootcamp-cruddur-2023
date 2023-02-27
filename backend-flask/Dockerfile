# https://github.com/omenking/aws-bootcamp-cruddur-2023/blob/week-1/journal/week1.md
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}


# Add Script file to docker file
COPY run.sh /backend-flask/run.sh

# Change to executable as root user
USER root
RUN chmod +x /backend-flask/run.sh

ENTRYPOINT ["sh","/backend-flask/run.sh"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]