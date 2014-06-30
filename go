#!/bin/bash

if [ ! -d pycortex/cortex ]; then
	echo "pycortex/cortex doesn't exist, initialising external repository..."
	git submodule init
	git submodule update
fi

source setpythonpath.sh
ipython -c "run main.py"
