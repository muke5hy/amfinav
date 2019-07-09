env=local
all: venv install

venv:
	virtualenv .venv -p python3

tests:
	pytest

install:
	echo "Installing packages from requirements.txt"
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python manage.py runserver $(port) 

clean:
	rm *.pyc

requirements:
	.venv/bin/pip freeze > requirements.txt

shell:
	.venv/bin/python

converage:
	.venv/bin/coverage run --source='.' manage.py test

zappa:
	.venv/bin/zappa 