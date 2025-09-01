FROM python:3.12.7
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --deploy --system 
COPY . .
RUN python /usr/src/app/business_card/manage.py collectstatic --noinput
RUN python /usr/src/app/business_card/manage.py migrate
RUN python /usr/src/app/business_card/manage.py loaddata business_card/author/fixtures/customeruser.json
RUN python /usr/src/app/business_card/manage.py loaddata business_card/author/fixtures/contact.json
CMD ["gunicorn", "--chdir", "/usr/src/app/business_card/", "-b", "0.0.0.0:8000", "business_card.wsgi:application"]
