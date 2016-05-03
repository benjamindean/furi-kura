all: clean run

clean:
	find furikura -type f -name *.pyc | xargs rm -rf
	find furikura -type d -name __pycache__ | xargs rm -rf
	rm -rf build/

run:
	bin/furikura

install:
	sudo python setup.py install --record uninstall.txt

uninstall:
	cat uninstall.txt | sudo xargs rm -rf