FROM python:3.8.0-slim-buster

ENV HOME=/home/docker_user

WORKDIR ${HOME}

ADD requirements.txt ${HOME}/requirements.txt
RUN pip install -r requirements.txt

ADD alembic.ini ${HOME}
COPY alembic/ ${HOME}/alembic
COPY scripts/ ${HOME}/scripts

COPY src/ ${HOME}/src
COPY tests/ ${HOME}/tests

RUN pip install -e ${HOME}/src

RUN mkdir /tmp/uwsgi

RUN useradd docker_user \
    && chown -R "docker_user:docker_user" ${HOME} \
    && chown -R "docker_user:docker_user" /tmp/uwsgi \
    && chmod g+r ${HOME} \
    && chmod 755 ${HOME}/scripts/*

USER docker_user