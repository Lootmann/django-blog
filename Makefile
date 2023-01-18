run:
	python3 manage.py runserver

.PHONY: reload
reload:
	python3 ./manage.py livereload

.PHONY: test
test:
	pytest -sv

.PHONY: cov
cov:
	coverage report

.PHONY: html
html:
	coverage html

.PHONY: dump
dump:
	python3 manage.py dumpdata> ./dump/data.yaml

.PHONY: req
req:
	pip freeze > requirements.txt
