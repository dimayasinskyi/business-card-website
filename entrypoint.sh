#!/bin/sh

python /usr/src/app/business_card/manage.py collectstatic --noinput
python /usr/src/app/business_card/manage.py migrate
python /usr/src/app/business_card/manage.py loaddata business_card/author/fixtures/customeruser.json
python /usr/src/app/business_card/manage.py loaddata business_card/author/fixtures/contact.json
exec gunicorn --chdir /usr/src/app/business_card/ business_card.wsgi:application --bind 0.0.0.0:8000
