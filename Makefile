all: clean run

VERSION=0.0.9

clean:
	find furikura -type f -name "*.pyc" | xargs rm -rf
	find . -type f -name "*.tar.gz" | xargs rm -rf
	find furikura -type d -name __pycache__ | xargs rm -rf
	rm -rf build/ dist/ deb_dist/ MANIFEST

run:
	bin/furikura

deb:
	cp README.md README
	python3 setup.py --command-packages=stdeb.command sdist_dsc
	cd deb_dist/furi-kura-$(VERSION)/ && dpkg-buildpackage -rfakeroot -uc -us

rpm:
	python3 setup.py bdist_rpm

version:
	sed -i 's/$(VERSION)/$(V)/g' setup.py Makefile README.md furikura/config.py furikura/ui/about.xml
	git add -A && git commit -m "Prepare $(V) release" && git push

release: deb
	git tag v$(VERSION) && git push --tags
	github-release release \
	--user benjamindean \
	--repo furi-kura \
	--tag v$(VERSION) \
	--name $(VERSION)
	github-release upload \
	--user benjamindean \
	--repo furi-kura \
	--tag v$(VERSION) \
	--name furi-kura-$(VERSION).tar.gz \
	--file furi-kura-$(VERSION).tar.gz
	github-release upload \
	--user benjamindean \
	--repo furi-kura \
	--tag v$(VERSION) \
	--name furi-kura_$(VERSION)-1_all.deb \
	--file deb_dist/furi-kura_$(VERSION)-1_all.deb

install:
	python3 setup.py install --record uninstall.txt

uninstall:
	cat uninstall.txt | xargs rm -rf
	rm uninstall.txt
