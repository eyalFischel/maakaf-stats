VENV_BIN = .venv/bin
PYTHON = $(VENV_BIN)/python3
PIP = $(VENV_BIN)/pip
REQUIREMENTS_PATH = requirements.txt

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install-deps   Install depedencies"
	@echo "  test           Run tests"
	@echo "  static-checks  Run static checks"
	@echo "  reformat       Reformat code"
	@echo "  clean          Clean up all generated files"
	@echo ""

.venv:
	python3 -m venv .venv

.PHONY: install-deps
install-deps: .venv
	$(PIP) install -r $(REQUIREMENTS_PATH)

.PHONY: test
test:
	$(PYTHON) -m pytest

.PHONY: static-checks
static-checks:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m pylint .
	$(PYTHON) -m black --check .

.PHONY: reformat
reformat:
	$(PYTHON) -m black .

.PHONY: clean
clean:
	rm -rf .venv