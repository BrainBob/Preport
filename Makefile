.PHONY: build up down logs migrate makemigrations createsuperuser shell seed lint

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

shell:
	docker compose exec backend python manage.py shell

seed:
	docker compose exec backend python manage.py seed_data

lint-backend:
	docker compose exec backend black . && flake8 .

lint-frontend:
	docker compose exec frontend npm run lint

lint: lint-backend lint-frontend
