.PHONY: sdist
sdist:
	python3.3 setup.py sdist

clean:
	-rm -f MANIFEST