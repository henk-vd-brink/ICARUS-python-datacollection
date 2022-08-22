FROM python:3.8.0-slim-buster

ENV HOME=/home/docker_user

RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    iputils-ping

WORKDIR ${HOME}

ADD requirements.txt ${HOME}/requirements.txt
RUN pip install -r requirements.txt

ADD alembic.ini ${HOME}
COPY alembic/ ${HOME}/alembic
COPY scripts/ ${HOME}/scripts

COPY src/ ${HOME}/src

RUN useradd docker_user \
    && chown -R "docker_user:docker_user" ${HOME} \
    && chmod g+r ${HOME} \
    && chmod 755 ${HOME}/scripts/*

USER docker_user