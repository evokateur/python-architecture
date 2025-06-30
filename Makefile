all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d app

down:
	docker-compose down

logs:
	docker-compose logs app | tail -100

flask:
	./flasker.sh run

unflask:
	./flasker.sh stop

test:
	pytest --tb=short

watch-tests:
	ls *.py | entr pytest --tb=short

black:
	black -l 86 $$(find * -name '*.py')
