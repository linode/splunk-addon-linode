build: clean getdeps
	./scripts/package.sh

clean:
	rm -f TA-linode/metadata/local.meta
	rm -rf TA-linode.tgz TA-linode/bin/deps

unittest:
	pytest TA-linode/bin/tests

getdeps:
	pip3 install -r requirements.txt --target TA-linode/bin/deps

lint:
    # Avoid linting pre-generated code
	pylint TA-linode/bin/tests TA-linode/bin/ta_linode_util

test: unittest