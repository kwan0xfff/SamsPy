#!/bin/sh

export PYTHONPATH=$(cd ..;pwd)/lib/
nosetests-3.2 .
