KEYWORD=FIXED

run: build
	docker run --rm keyword-release-action --keyword $(KEYWORD)

build:
	docker build --tag keyword-release-action .

test:
	python3 ./entrypoint.py --keyword $(KEYWORD)
