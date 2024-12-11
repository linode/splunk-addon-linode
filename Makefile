PYTHON := python

build: clean getdeps
	slim package TA-linode

clean:
	rm -rf TA-linode*.tar.gz TA-linode/bin/deps TA-linode/metadata/local.meta

unittest:
	pytest TA-linode/bin/tests

getdeps:
	$(PYTHON) -m pip install -r requirements-dev.txt --break-system-packages
	$(PYTHON) -m pip install -r requirements.txt --upgrade --target TA-linode/bin/deps --break-system-packages

lint:
    # Avoid linting pre-generated code
	pylint TA-linode/bin/tests TA-linode/bin/ta_linode_util

test: unittest
