build:
	docker-compose build

up:
	docker-compose up -d

start:
	docker-compose start

stop:
	docker-compose stop

data:
	docker volume create --name=pharos-data

shell-nginx:
	docker exec -ti ng01 bash

shell-web:
	docker exec -ti dg01 bash

shell-db:
	docker exec -ti ps01 bash

log-nginx:
	docker-compose logs nginx  

log-web:
	docker-compose logs web  

log-ps:
	docker-compose logs postgres

log-rmq:
	docker-compose logs rabbitmq

log-worker:
	docker-compose logs worker
