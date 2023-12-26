CONTAINER_NAME = app
RUN_APP = docker-compose exec $(CONTAINER_NAME)
RUN_POETRY =  $(RUN_APP) poetry run
RUN_DJANGO = $(RUN_POETRY) python manage.py
RUN_PYTEST = $(RUN_POETRY) pytest
RUN_NPM = npm run 
FRONTEND_PATH = --prefix frontend
RUN_TERRAFORM = docker-compose -f infra/docker-compose.yml run --rm terraform

prepare:
	npm install
	docker-compose up -d --build

up:
	docker-compose up -d

build:
	docker-compose build

install:
	npm install $(FRONTEND_PATH)

down:
	docker-compose down

loaddata:
	$(RUN_DJANGO) loaddata fixture.json

makemigrations:
	$(RUN_DJANGO) makemigrations

migrate:
	$(RUN_DJANGO) migrate

show_urls:
	$(RUN_DJANGO) show_urls

shell:
	$(RUN_DJANGO) debugsqlshell

superuser:
	$(RUN_DJANGO) createsuperuser

test:
	$(RUN_PYTEST)

format:
	$(RUN_POETRY) black .
	$(RUN_POETRY) isort .
	$(RUN_NPM) format $(FRONTEND_PATH)

update:
	$(RUN_APP) poetry update
	npm update $(FRONTEND_PATH)

db:
	docker exec -it db bash

pdoc:
	$(RUN_APP) env CI_MAKING_DOCS=1 poetry run pdoc -o docs application


collectstatic:
	$(RUN_DJANGO) collectstatic

init:
	$(RUN_TERRAFORM) init

fmt:
	$(RUN_TERRAFORM) fmt

validate:
	$(RUN_TERRAFORM) validate

show:
	$(RUN_TERRAFORM) show

apply:
	$(RUN_TERRAFORM) apply -auto-approve

destroy:
	$(RUN_TERRAFORM) destroy