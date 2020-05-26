PY3 = python3
PIP3 = pip3


default: install

clean:
	rm -f dist/*
	rm -rf build/*
		
install: clean pkg
	$(PY3)  setup.py install

pkg: clean
	$(PY3) setup.py sdist bdist_wheel

uninstall: clean
	$(PIP3) uninstall threefive
	
upload: clean pkg	
	twine upload dist/*

upgrade:
	$(PIP3) install --upgrade threefive
	
