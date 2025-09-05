FROM python:3.12.7
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --deploy --system 
COPY . .

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]