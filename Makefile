MANAGE_PATH='./backend'

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help: ## вывод доступных команд
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

setup: ## mkmigrations migrate suser run
setup: mkmigrations migrate suser load run

mkmigrations: ## makemigrations
mkmigrations:
	cd $(MANAGE_PATH); python3 manage.py makemigrations

migrate: ## migrate
migrate:
	cd $(MANAGE_PATH); python3 manage.py migrate

suser: ## createsuperuser
suser:
	cd $(MANAGE_PATH); python3 manage.py createsuperuser

load: ## load initial data
load:
	cd $(MANAGE_PATH); python3 manage.py load_ingredients_data

run: ## runserver
run:
	cd $(MANAGE_PATH); python3 manage.py runserver

clean: ## очистить кэш, удалить миграции, удалить бд
clean: rmmigrations rmdb rmcache

rmcache: ## очистка кэша
rmcache:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf

rmdb: ## удалить бд
rmdb:
	find . | grep -E db.sqlite3 | xargs rm -f

rmmigrations: ## удалить миграции
rmmigrations:
	find ./backend/ | grep -E 000* | xargs rm -f
