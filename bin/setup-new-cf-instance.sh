#!/usr/bin/env sh

# set -x

if [ $# -ne 1 ]
then
    echo "usage: $0 app-name"
    exit 1
fi
APP_NAME="$1"

# sanity check: the manifest.yml must match the app name
# we do not check the route or service names because these can change.
OUTPUT=`grep -e "^- name: $APP_NAME$" manifest.yml`
if [ $? -ne 0 ]
then
    echo "please set the manifest.yml name to $APP_NAME first."
    echo "(you probably also want to change the route and service names)."
    exit 1
fi

# bail out early if we can't generate a secret key
SECRETKEY=`python -c 'from django.core.management.utils import get_random_secret_key as grsk; print(grsk())'`
if [ $? -ne 0 ]
then
    echo "please install this repo's python dependencies first."
    exit 1
fi

cf target
if [ $? -ne 0 ]
then
    echo "please login cf first."
    exit 1
fi

read -p "If this is your desired target, hit enter (Control-C to exit): " accepted

cf create-service aws-rds shared-psql ${APP_NAME}-db
cf create-service s3 basic-public-sandbox ${APP_NAME}-s3
cf push $APP_NAME --no-start
cf bind-service $APP_NAME ${APP_NAME}-db
cf bind-service $APP_NAME ${APP_NAME}-s3
# note: DEBUG=1 is required to deploy static files
cf set-env $APP_NAME DEBUG 1
cf set-env $APP_NAME DISABLE_COLLECTSTATIC 1
cf set-env $APP_NAME DJANGO_SETTINGS_MODULE: distiller.settings.production
read -p "Django admin: Enter your email: " email
cf set-env $APP_NAME DJANGO_SUPERUSER_EMAIL $email
read -p "Django admin: Enter your username: "  username
cf set-env $APP_NAME DJANGO_SUPERUSER_USERNAME $username
read -s -p "Django admin: Enter your password (will not be shown): " password
cf set-env $APP_NAME DJANGO_SUPERUSER_PASSWORD $password
cf set-env $APP_NAME SECRET_KEY $SECRETKEY
cf restage $APP_NAME
cf start $APP_NAME
