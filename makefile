.PHONY: all setup static db example superuser
# make tests >debug.log 2>&1
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

DJANGO_VER = 4

SOURCE = django_admin_geomap
TESTS = tests
CFG_TEST = example.settings

FLAKE8 = $(PYTHON) -m flake8 --max-line-length=120
PYLINT = $(PYTHON) -m pylint
PYTEST = $(PTEST) -c pytest$(DJANGO_VER).ini --cov=$(SOURCE) --cov-report term:skip-covered
MANAGE = $(PYTHON) manage.py
PIP = $(PYTHON) -m pip install
SETTINGS = --settings $(CFG_TEST)
MIGRATE = $(MANAGE) makemigrations $(SETTINGS)

all: tests

test:
	$(PTEST) -s $(TESTS)/test/$(T)

flake8:
	$(FLAKE8) $(SOURCE)
	$(FLAKE8) $(TESTS)/test

lint:
	$(PYLINT) $(TESTS)/test
	$(PYLINT) $(SOURCE)

pep257:
	$(PYTHON) -m pydocstyle $(SOURCE)
	$(PYTHON) -m pydocstyle --match='.*\.py' $(TESTS)/test

tests: flake8 pep257 lint static db
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

example:
	$(MANAGE) runserver $(SETTINGS)

superuser:
	$(MANAGE) createsuperuser $(SETTINGS)

db:
	$(MIGRATE) example
	$(MANAGE) migrate $(SETTINGS)

static:
	$(MANAGE) collectstatic --noinput $(SETTINGS)

package:
	$(PYTHON) -m build -n

pypitest: package
	$(PYTHON) -m twine upload --config-file .pypirc --repository testpypi dist/*

pypi: package
	$(PYTHON) -m twine upload --config-file .pypirc dist/*

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r $(TESTS)/requirements.txt
	$(PIP) -r $(TESTS)/django$(DJANGO_VER).txt
	$(PIP) -r deploy.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
