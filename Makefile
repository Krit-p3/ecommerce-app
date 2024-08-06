WORKDIR := src/

dev:
	cd $(WORKDIR) && poetry run uvicorn main:app --reload


test: 
	# add pytest 
	echo "testing ..." 

lint:
	# add linting 
	poetry run ruff check --fix $(WORKDIR)

format: 
	# add format
	poetry run ruff format $(WORKDIR)
