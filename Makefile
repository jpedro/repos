
.PHONY: build
build: ### Builds this package
	python setup.py sdist

.PHONY: next
next: ### Bumps into the next version
	@echo "Next version: $(shell git next)"
	@echo "VERSION = \"$(shell git next)\"" > repos/__init__.py

.PHONY: upload
upload: build ### Publishes a new version
	### This expects this file set up:
	###     $ cat ~/.pypirc
	###     [pypi]
	###       username = __token__
	###       password = pypi-xxx
	python -m twine upload dist/*
