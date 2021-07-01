build:
	./scripts/package.sh

clean:
	rm -rf TA-linode.tgz TA-linode/bin/deps

unittest:
	pytest TA-linode/bin/tests

test: unittest