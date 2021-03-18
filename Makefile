ROOT_DIR:=./
SRC_DIR:=./src
VENV_BIN_DIR:="venv/bin"

REQUIREMENTS_DIR:"requirements"
REQUIREMENTS_LOCAL:"$(REQUIREMENTS_DIR)/local.txt"

PIP:="$(VENV_BIN_DIR)/pip"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python")

install:
	@$(create-venv)
	@$(PIP) install -r $(REQUIREMENTS_LOCAL)

clean:
	@rm -rf .cache
	@find . -type d -name __pycache__ -delete