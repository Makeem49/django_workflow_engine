#!/bin/bash

NAME="workflow"
DIR=/home/workflow_engine/workflow_engine/src
USER=workflow_engine
GROUP=workflow_engine
WORKERS=3
BIND=unix:/home/workflow_engine/workflow_engine/app.sock
DJANGO_SETTINGS_MODULE=app.settings
DJANGO_WSGI_MODULE=app.wsgi
LOG_LEVEL=error

cd $DIR
source ./venv/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec ../workflow_engine/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
