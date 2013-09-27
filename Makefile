################################################
# Makefile for AsyncKit.py with release helper #
################################################
SHELL := /bin/bash
usage: ;
	# Usage:
	#   make test      - run test suite
	#   make install   - install dependencies
	#   make release   - release to pypi (remember to bump version)

test: ;
	nosetests -v -d --with-coverage -w ${CURDIR}

install: ;
	cd ${CURDIR}
	pip install -r requirements.txt

.version_notice: ;
	@echo "Remembered to bump the version?!"

.set_pypirc: .version_notice ;
	#creates the ~/.pypirc file for release
	@echo -e "\
[distutils] \n\
index-servers =\n\
    pypi\n\
    \n\
[pypi]\n\
username:$(shell if [ -z $(user) ] ; then read -p "PyPI User: " REPLY ; echo $$REPLY ; fi )\n\
password:$(shell if [ -z $(password) ] ; then read -s -p "PyPI Pass: " REPLY ; echo $$REPLY ; fi )\n\
" > ~/.pypirc

.unset_pypirc: ;
	@rm ~/.pypirc

.do_release: ;
	python setup.py register
	python setup.py sdist upload

release: .set_pypirc .do_release .unset_pypirc ;
