build:
	hatch build
install:
	pip install --force-reinstall dist/scribo*.whl
build-install:
	make build
	make install
format:
	djlint --reformat src/scribo/project_template/assets/templates/*html.jinja
	black src/scribo/
	black tests/
