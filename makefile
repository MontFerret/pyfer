ifndef GO_LIB_PATH
	GO_LIB_PATH=./lib/
endif
ifndef BIN
	BIN=./bin/
endif
ifndef TAR
	TAR=tar
endif
ifndef GO
	GO=go
endif
ifndef GIT
	GIT=git
endif
ifndef PYTHON
	PYTHON=python
endif
ifndef GO_VERSION
	GO_VERSION=1.16.3
endif
ifndef GO_ARCHITECTURE
	GO_ARCHITECTURE=amd64
endif
ifndef GO_OS
	GO_OS=linux
endif
ifndef GO_URL
	GO_URL=https://golang.org/dl/go${GO_VERSION}.${GO_OS}-${GO_ARCHITECTURE}.tar.gz
endif
ifndef WGET
	WGET=wget
endif
ifndef RM
	RM=rm
endif
ifndef GO_INSTALLER
	GO_INSTALLER=go-installer
endif
ifndef GO_COMPILER_PATH
	GO_COMPILER_PATH=${BIN}go/bin/
endif
ifndef VERSION
	VERSION=$(shell cat version)
endif

build: deps
	$(info ${GO} version)
	PATH=`pwd`${GO_COMPILER_PATH}:${PATH}
	${GO} build -buildmode c-shared -o ${GO_LIB_PATH}libferret.so ${GO_LIB_PATH}

clean:
	#${GIT} checkout master
	#${GIT} fetch
	#${GIT} pull origin master
	#${GIT} branch -D ${VERSION}
	${RM} -rf
	${RM} -rf ${BIN} dist pferret.egg-info dist build

deps: clean
	$(info go-version: ${GO_VERSION})
	$(info go-architecture: ${GO_ARCHITECTURE})
	$(info go-os: ${GO_OS})
	mkdir ${BIN}
	${WGET} -P ${BIN} ${GO_URL} -O ${BIN}${GO_INSTALLER}
	${TAR} -C ${BIN} -xzf ${BIN}${GO_INSTALLER}
	${RM} ${BIN}${GO_INSTALLER}

publish-package:
	git checkout -b release-${VERSION}
	git add .
	git commit -m "[version]. ${cat $(VERSION)}"
	git push origin release-${VERSION}
	$(PYTHON) setup.py bdist_wheel upload -r ferret
