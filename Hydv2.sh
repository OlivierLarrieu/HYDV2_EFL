#!/bin/bash

export LD_LIBRARY_PATH=$PWD/EFL1.9/lib/:$PWD/lib/
python2.7 main.py

echo "exit Hydv2"
exit 0
