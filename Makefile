.PHONY: help
help: ### Shows this help
	@grep -E '^[0-9a-zA-Z_-]+:' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?### "}; {printf "\033[32;1m%-16s\033[0m %s\n", $$1, $$2}'


.PHONY: build
build: ### Builds this package
	python3 setup.py sdist


.PHONY: clean
clean: ### Cleans this stuff
	rm -fr dist
	rm -fr build
	rm -fr *.egg-info

# .PHONY: next
# next: ### Bumps into the next version
# 	@echo "Next version: $(shell git next)"
# 	@echo "VERSION = \"$(shell git next)\"" > repos/__init__.py


.PHONY: go
go: build ### Publishes a new version
	### This expects this file set up:
	###     $ cat ~/.pypirc
	###     [pypi]
	###       username = __token__
	###       password = pypi-xxx
	python3 -m twine upload dist/*
