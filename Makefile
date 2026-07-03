# Conda environment configuration
ENV_NAME = viettel-ai-race

.PHONY: help create update clean activate info download

help:
	@echo "======================================================================"
	@echo "Viettel AI Race 2026 - Environment Management Commands"
	@echo "======================================================================"
	@echo "make create      : Create the Conda environment from environment.yml"
	@echo "make update      : Update the Conda environment and prune unused packages"
	@echo "make clean       : Remove the Conda environment"
	@echo "make info        : Show details about the Conda environment"
	@echo "make activate    : Show how to activate the Conda environment"
	@echo "make download    : Download the Qwen/Qwen3.5-2B model weights using HF_TOKEN from .env"
	@echo "======================================================================"

create:
	conda env create -f environment.yml

update:
	conda env update -f environment.yml --prune

clean:
	conda env remove -n $(ENV_NAME) -y

info:
	conda env list
	-conda list -n $(ENV_NAME)

download:
	conda run -n $(ENV_NAME) python download_model.py

activate:
	@echo "======================================================================"
	@echo "To activate the environment, run the following command in your terminal:"
	@echo "======================================================================"
	@echo "  conda activate $(ENV_NAME)"
	@echo "======================================================================"
