CONTAINER_NAME = app
RUN_APP = docker-compose exec $(CONTAINER_NAME)
RUN_POETRY =  $(RUN_APP) poetry run
RUN_DJANGO = $(RUN_POETRY) python manage.py
RUN_PYTEST = $(RUN_POETRY) pytest
RUN_TERRAFORM = docker-compose -f infra/docker-compose.yml run --rm terraform

up:
	docker-compose up -d

build:
	docker-compose build

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

test-cov:
	$(RUN_PYTEST) --cov=application/tests/

loadtest:
	$(RUN_PYTEST) --alluredir=allure-results
	sh send_results.sh

format:
	$(RUN_POETRY) black .
	$(RUN_POETRY) isort .

update:
	$(RUN_APP) poetry update

db:
	docker exec -it db bash

pdoc:
	$(RUN_APP) env CI_MAKING_DOCS=1 poetry run pdoc -o docs application

vault:
	aws-vault exec $(IAM_USER) --duration=$(DURATION)

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

graph:
	$(RUN_TERRAFORM) graph | dot -Tsvg > graph.svg

destroy:
	$(RUN_TERRAFORM) destroy