VENV_BIN = .venv/bin
PYTHON = $(VENV_BIN)/python3
PIP = $(VENV_BIN)/pip
REQUIREMENTS_PATH_DISCORD = discord_bot/requirements.txt
REQUIREMENTS_PATH_AIRFLOW = airflow/scripts/git_scripts/requirements.txt
CODE_DIR = ./

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

.PHONY: .venv
.venv:
	python3 -m venv .venv

.PHONY: install-deps
install-deps: .venv
	$(PIP) install -r $(REQUIREMENTS_PATH_DISCORD) && $(PIP) install -r $(REQUIREMENTS_PATH_AIRFLOW)

.PHONY: test
test:
	$(PYTHON) -m pytest

.PHONY: static-checks
static-checks:
	$(PYTHON) -m flake8 $(CODE_DIR)
	$(PYTHON) -m pylint $(CODE_DIR) --recursive=true
	$(PYTHON) -m black --check --exclude .venv .

.PHONY: reformat
reformat:
	$(PYTHON) -m black --exclude .venv .
	$(PYTHON) -m isort --skip .venv .
	$(PYTHON) -m autoflake --in-place --remove-all-unused-imports --recursive --exclude .venv .


.PHONY: clean
clean:
	rm -rf .venv