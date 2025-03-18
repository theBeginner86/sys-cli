.IPHONY: deps build

deps:
	sudo apt-get update;
	sudo apt-get install libelf-dev cmake clang llvm llvm-dev python-is-python3 -y;
	git clone --recursive https://github.com/intel/processwatch.git;
	cd processwatch;
	/bin/bash build.sh; sudo cp ./processwatch /usr/local/bin;
	cd ..;


build:
	go build -o systat .
