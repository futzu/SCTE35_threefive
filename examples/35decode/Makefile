PY3 = python3
PYPY3 = pypy3

default: cli

	
cli:
	sed -i s/$(PYPY3)/$(PY3)/ 35decode
	install 35decode /usr/local/bin
	
pypy3-cli:
	sed -i s/$(PY3)/$(PYPY3)/ 35decode
	install 35decode /usr/local/bin


