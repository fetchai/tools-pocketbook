#!/bin/bash
set -e

# remove the old dist folders
rm -Rf dist/ build/

# build the package
python3 setup.py sdist bdist_wheel

# upload the packages
twine upload dist/*
