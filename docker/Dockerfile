FROM python:3.11-alpine

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml main.py /app/
COPY app app

RUN poetry config virtualenvs.create false --local && \
    poetry install

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "app:app" ]
