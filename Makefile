.PHONY: all version v install i test t build b dist d clean c

all: clean install test build version

version v:
	git describe --tags ||:
	python -m setuptools_scm

test t:
	pytest --cov=src/cedartl tests/ --cov-report term-missing

install i:
	pip install --upgrade --force-reinstall -e .

build b:
	# SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
	python -m build

dist d: clean test build
	scripts/check-version.sh
	twine upload dist/*

clean c:
	rm -rfv out dist build/bdist.*
