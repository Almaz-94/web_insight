runserver:
	python manage.py runserver 0:8001

run_listener:
	python -m main.nats_listener.listener_runner

migrate:
	python manage.py migrate

start_app: migrate  runserver
#
#.PHONY: help
#
#help: # Run `make help` to get help on the make commands
#	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
