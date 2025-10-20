
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
	@echo "Docs generation can be wired to Widoco or OnToology in CI."

