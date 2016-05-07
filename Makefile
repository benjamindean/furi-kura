all: clean run

VERSION=0.0.1

clean:
	find furikura -type f -name *.pyc | xargs rm -rf
	find furikura -type d -name __pycache__ | xargs rm -rf
	sudo rm -rf build/ dist/ deb_dist/ MANIFEST

run:
	bin/furikura

deb:
	python3 setup.py --command-packages=stdeb.command sdist_dsc 
	--with-python3=True -m="Benjamin Dean" --package="furi-kura" --depends="python3-flask, python3-requests"
	cd deb_dist/furi-kura-$(VERSION)/ && dpkg-buildpackage -rfakeroot -uc -us

rpm:
	python3 setup.py bdist_rpm

version:
	sed -i 's/$(VERSION)/$(RELEASE)/g' setup.py Makefile

install:
	sudo python3 setup.py install --record uninstall.txt

uninstall:
	cat uninstall.txt | sudo xargs rm -rf
	sudo rm uninstall.txt
