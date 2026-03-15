install:
pip install -r requirements.txt

test:
PYTHONPATH=. pytest

docker-run:
docker-compose up --build

clean:
rm -rf __pycache__ .pytest_cache test.db
