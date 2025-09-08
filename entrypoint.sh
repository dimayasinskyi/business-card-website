#!/bin/sh

python /usr/src/app/business_card/manage.py collectstatic --noinput
python /usr/src/app/business_card/manage.py migrate
python /usr/src/app/business_card/manage.py loaddata business_card/author/fixtures/customeruser.json
python /usr/src/app/business_card/manage.py loaddata business_card/author/fixtures/contact.json

gunicorn --chdir /usr/src/app/business_card/ business_card.wsgi:application --bind 0.0.0.0:8000 &
WEB_PID=$!
echo "Django is running"

sleep 3

celery --workdir /usr/src/app/business_card/ -A business_card worker --loglevel=info &
WORKER_PID=$!

celery --workdir /usr/src/app/business_card/ -A business_card beat --loglevel=info &
BEAT_PID=$!
echo "Celery is running"

while true; do
    for pid in $WEB_PID $WORKER_PID $BEAT_PID; do
        if ! kill -0 $pid 2>/dev/null; then
            EXIT_CODE=1
            echo "Process $pid exited. Stopping others..."
            kill -TERM $WEB_PID $WORKER_PID $BEAT_PID 2>/dev/null || true
            exit $EXIT_CODE
        fi
    done
    sleep 1
done