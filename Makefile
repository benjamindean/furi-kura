all: clean run

VERSION=0.0.4

clean:
	find furikura -type f -name *.pyc | xargs rm -rf
	find . -type f -name *.tar.gz | xargs rm -rf
	find furikura -type d -name __pycache__ | xargs rm -rf
	sudo rm -rf build/ dist/ deb_dist/ MANIFEST

run:
	bin/furikura

deb:
	python3 setup.py --command-packages=stdeb.command sdist_dsc
	cd deb_dist/furi-kura-$(VERSION)/ && dpkg-buildpackage -rfakeroot -uc -us

rpm:
	python3 setup.py bdist_rpm

version:
	sed -i 's/$(VERSION)/$(V)/g' setup.py Makefile
	git add -A && git commit -m "Prepare $(V) release"

install:
	sudo python3 setup.py install --record uninstall.txt

uninstall:
	cat uninstall.txt | sudo xargs rm -rf
	sudo rm uninstall.txt
