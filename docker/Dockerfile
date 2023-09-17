FROM python:3.11-alpine

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY main.py main.py
COPY app app

RUN pip3 install -r requirements.txt

ENV FLASK_APP main.py

# gunicorn -w 4 -b 0.0.0.0:5000 --log-level info --access-logfile - --error-logfile - app:app
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "app:app" ]
