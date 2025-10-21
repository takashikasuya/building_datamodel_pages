
    .PHONY: setup build validate test docs

    setup:
	pip install -r requirements.txt

    build:
	python -m src.cli build

    validate:
	python -m src.cli validate-rdf
	python -m src.cli validate-shacl

    test:
	pytest -q

    docs:
	python -m src.cli docs

