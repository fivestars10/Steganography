install:
	@pip install -r requirements/local.txt

clean:
	@rm -rf .cache
	@find . -type d -name __pycache__ -delete