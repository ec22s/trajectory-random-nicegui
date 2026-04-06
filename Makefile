.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

down:
	@docker compose down -v --volumes --remove-orphans

dev:
	@docker compose up --build -d
