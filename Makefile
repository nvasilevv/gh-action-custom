KEYWORD=FIXED

run: build
	docker run --rm keyword-release-action $(KEYWORD)

build:
	docker build --tag keyword-release-action .

test:
	python3 ./entrypoint.py $(KEYWORD)
