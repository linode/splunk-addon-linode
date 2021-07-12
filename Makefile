build: clean
	./scripts/package.sh

clean:
	rm -f TA-linode/metadata/local.meta
	rm -rf TA-linode.tgz TA-linode/bin/deps

unittest:
	pytest TA-linode/bin/tests

test: unittest