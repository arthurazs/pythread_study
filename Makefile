server:
	python server.py

install:
	pip install uv

build:
	uv pip install .

lint:
	mypy .
	ruff check .

default: threading

threading:
	python default.py

pool:
	python pool.py

clean:
	rm -rf .ruff_cache build .mypy_cache threading_study.egg-info

