build: clean getdeps
	slim package TA-linode

clean:
	rm -rf TA-linode*.tar.gz TA-linode/bin/deps TA-linode/metadata/local.meta

unittest:
	pytest TA-linode/bin/tests

getdeps:
	pip install -r requirements-dev.txt
	pip install -r requirements.txt --target TA-linode/bin/deps

lint:
    # Avoid linting pre-generated code
	pylint TA-linode/bin/tests TA-linode/bin/ta_linode_util

test: unittest