run: 
	@uvicorn workout_api.main:app --reload

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head

stop-postgres:
	@sudo service postgresql stop

start-docker:
	@docker-compose up -d

check-docker:
	@docker ps