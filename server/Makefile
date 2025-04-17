venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && uvicorn main:app --reload