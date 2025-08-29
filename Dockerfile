FROM python:3.12.7
WORKDIR /usr/src/app
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system 
COPY . .
CMD ["gunicorn", "--chdir", "/usr/src/app/business_card/", "-b", "0.0.0.0:8000", "business_card.wsgi:application"]
