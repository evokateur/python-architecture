FROM python:3.13-slim-buster

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code

ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80
# ENV PYTHONUNBUFFERED=1
# CMD uvicorn fast_api_app:app --host 0.0.0.0 --port 80
