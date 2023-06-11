FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY backend/pyproject.toml /code/
# Initialize python project with Poetry
RUN pip install --upgrade pip && pip install poetry
RUN poetry install

COPY ./containers/django/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
