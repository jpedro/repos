.PHONY: build
build: ### Builds this package
	python setup.py sdist


.PHONY: upload
upload: build ### Publishes a new version
	python -m twine upload dist/*


### This expects this file set up:
###     $ cat ~/.pypirc
###     [pypi]
###       username = __token__
###       password = pypi-xxx
