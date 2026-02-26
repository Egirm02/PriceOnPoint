.PHONY: test test-e2e run

test:
	pytest -q -m "not e2e"

test-e2e:
	pytest -q -m e2e

run:
	python -m weeklyad --source both --zip 94611 --out-dir output
