FROM python:3.8.3-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app

# Install packages neccessary to build
RUN apt-get -y -qq update &&\
    apt-get -y -qq install libpq-dev gcc netcat

# Install pip and Python dependencies
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

# Install npm and JS dependencies
RUN apt-get -y -qq install npm &&\
    npm install --save &&\
    npm run build

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]