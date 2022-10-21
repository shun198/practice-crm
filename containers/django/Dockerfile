FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY . /code/
RUN pip install --upgrade pip && pip install poetry
RUN poetry install
