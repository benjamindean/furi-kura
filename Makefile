all: clean run

clean:
	find furikura -type f -name *.pyc | xargs rm -rf
	find furikura -type d -name __pycache__ | xargs rm -rf
	sudo rm -rf build/ dist/ deb_dist/ MANIFEST

run:
	bin/furikura

deb:
	python setup.py sdist
	py2dsc-deb dist/furi-kura-*.tar.gz

install:
	sudo python setup.py install --record uninstall.txt

uninstall:
	cat uninstall.txt | sudo xargs rm -rf
	sudo rm uninstall.txt