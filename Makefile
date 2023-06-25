.PHONY: format

format:
	black .
	ruff --select I --fix .