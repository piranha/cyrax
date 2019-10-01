pub:
	rm -rf dist
	./setup.py sdist
	twine upload dist/*
