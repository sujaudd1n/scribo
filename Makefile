build:
	hatch build
install:
	pip install --force-reinstall dist/scribo*.whl
bi:
	make build
	make install
