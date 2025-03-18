build:
	hatch build
install:
	pip install --force-reinstall dist/scribo*.whl
build-install:
	make build
	make install
fmt:
	black src/scribo/
	black tests/
	djlint --reformat src/scribo/**/*html.jinja
lint:
	python -m flake8 src/scribo
test:
	pytest
