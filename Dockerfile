FROM python:3.7-alpine
RUN pip install pipenv
ADD . /app
WORKDIR /app
RUN pipenv install --system
RUN pip install gunicorn[gthread]
EXPOSE 5000
CMD gunicorn --worker-class gthread --workers 1 --threads 40 --bind 0.0.0.0:5000 wsgi:app --keep-alive 5 --log-level info