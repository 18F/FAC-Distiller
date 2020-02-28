#/bin/bash

set -o errexit
set -o pipefail

# Only run migrations on the zeroth index when in a cloud.gov environment
if [[ -v CF_INSTANCE_INDEX && $CF_INSTANCE_INDEX == 0 ]]
then
  python manage.py migrate --settings=distiller.settings.production --noinput
else
  echo "Migrations did not run."
  if [[ -v CF_INSTANCE_INDEX ]]
  then
    echo "CF Instance Index is ${CF_INSTANCE_INDEX}."
  fi
fi

# Ensure a superuser exists. These environment variables are required:
# DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD, DJANGO_SUPERUSER_EMAIL
python manage.py createsuperuser --noinput || true

# Collect static files
python manage.py collectstatic --settings=distiller.settings.production --noinput

# Run gunicorn wsgi server
gunicorn -k gevent -w 2 distiller.wsgi:application
