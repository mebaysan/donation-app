.PHONY: help

help:
	@echo "Donation Backend"
	@echo "~~~~~~~~~~~~~~~"
	@echo ""
	@echo "check        : Health check"
	@echo "coverage     : Make test coverage"
	@echo "docup        : Run docker compose services"
	@echo "docdown      : Stop docker containers"
	@echo "migrations   : Make django migrations"
	@echo "install      : Install python requirements"
	@echo "recover      : docdown + docup + wait + migrations + loaddata"
	@echo "runserver    : Run django server in debug mode"
	@echo "run_gunicorn : Run django server with gunicorn"
	@echo "static       : Collect static files"
	@echo "superuser    : Create django super user"
	@echo "test         : Start django test runner"
	@echo "translation  : Translation operation"
	@echo "wait         : Wait for 3 seconds"
	@echo ""

check:
	@python manage.py check

docup:
	@docker compose up -d --build

docdown:
	@docker compose down -v

dumpdata:
	@python manage.py dumpdata -o dummy.json

loaddata:
	@python manage.py loaddata scripts/dummy.json

migration:
	@python src/manage.py makemigrations
	@python src/manage.py migrate

install:
	@pip install --upgrade pip
	@pip install -r src/requirements.txt

recover: install docdown docup wait migration loaddata
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

recover_refactor: install docdown docup wait migration superuser
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

runserver:
	@python src/manage.py runserver 127.0.0.1:8000

run_gunicorn:
	@gunicorn src/donation.wsgi:application --bind 0.0.0.0:8000

collect:
	@python src/manage.py collectstatic --no-input

superuser:
	@python src/manage.py createsuperuser

translation:
	@python manage.py makemessages -l tr
	@python manage.py compilemessages

wait:
	@sleep 3

create-devdb:
	@bash ./scripts/dev-postgres.sh

start-devdb:
	@docker container start donation_database_dev

stop-devdb:
	@docker container stop donation_database_dev

rm-devdb:
	@docker rm -f -v donation_database_dev
	@docker volume rm donation_database_dev

runproxyversion:
	@make collect
	@make migration
	@make run_gunicorn

format:
	@black src

lint:
	@flake8 src

test:
	@pytest src/ -vv --disable-warnings --cov

coverage:
	@coverage report -m
	@coverage html
	@coverage xml

load_countries_states:
	@python src/manage.py load_countries_states
