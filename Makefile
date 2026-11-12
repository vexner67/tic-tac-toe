# Makefile для удобной работы с проектом «Крестики-нолики».

PYTHON  ?= python3
VENV    := .venv
BIN     := $(VENV)/bin
PY      := $(BIN)/python

.PHONY: venv install run test coverage lint check clean

venv: ## Создать виртуальное окружение
	$(PYTHON) -m venv $(VENV)

install: venv ## Установить зависимости
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

run: venv ## Запустить приложение
	$(PY) -m tic_tac_toe

test: ## Запустить тесты
	$(PY) -m pytest

coverage: ## Запустить тесты с отчётом о покрытии
	@coverage_dir=$$(mktemp -d); \
	trap 'rm -rf "$$coverage_dir"' EXIT; \
	COVERAGE_FILE="$$coverage_dir/.coverage" $(PY) -m pytest \
		--cov=tic_tac_toe --cov-report=term-missing

lint: ## Проверить код на соответствие PEP 8
	$(PY) -m flake8 tic_tac_toe tests

check: lint test ## Линтер + тесты
