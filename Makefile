
test: ;
	nosetests -v -d --with-coverage -w ${CURDIR}

install: ;
	cd ${CURDIR}
	pip install -r requirements.txt