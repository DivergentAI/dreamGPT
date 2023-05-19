.PHONY:start
start:
	docker-compose up --build -d

.PHONY:stop
stop:
	docker-compose down