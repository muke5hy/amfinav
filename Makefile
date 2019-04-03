env=local
all: venv install

bootstrap: 
	echo "Installing Pip"
	sudo apt-get install pyenv
	sudo apt-get install python-pip
	echo "Installing virtualenv"
	sudo pip install virtualenv
	sudo pip install nose

venv:
	virtualenv .venv -p python3

npm: 
	npm install
tests:
	export APP_SETTINGS=config.TestingConfig
	nosetests -v tests

install:
	echo "Installing packages from requirements.txt"
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python manage.py runserver $(port) 

clean:
	rm *.pyc

requirements:
	.venv/bin/pip freeze > requirements.txt

manage:
	.venv/bin/python manage.py $(command) 

shell:
	.venv/bin/python

converage:
	.venv/bin/coverage run --source='.' manage.py test

collectstatic:
	.venv/bin/python manage.py collectstatic

zappa:
	.venv/bin/zappa 