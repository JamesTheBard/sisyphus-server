FROM python:3.11-alpine

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY main.py main.py
COPY app app

RUN pip3 install -r requirements.txt

ENV FLASK_APP main.py

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0", "app:app" ]
