#!/bin/sh

python /usr/src/app/business_card/manage.py collectstatic --noinput
exec gunicorn --chdir /usr/src/app/business_card/ business_card.wsgi:application --bind 0.0.0.0:8000 