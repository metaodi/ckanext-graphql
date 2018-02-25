#!/bin/sh -e

# Check PEP-8 code style and McCabe complexity
flake8 --statistics --show-source ckanext

# run tests
nosetests --ckan --nologcapture --with-pylons=subdir/test.ini --verbose ckanext/graphql
