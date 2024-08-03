WORKDIR := src/

dev:
	cd $(WORKDIR) && poetry run uvicorn main:app --reload


test: 
	# add pytest 
	echo "testing ..." 

lint:
	# add linting 
	echo "linting ..."

format: 
	# add format
	echo "formating ..."
