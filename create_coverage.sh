#!/bin/bash
set -o errexit

export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

# remove any old data.
coverage erase 
rm -rf .coverage.*

# run all tests (but only collect the coverage of the tests)
# this makes sure all tests have been run and discover does
# not miss one.
coverage run --source=tests `which django-admin.py` test 
mv .coverage .coverage.functional

# run unit tests.
# We only want to have the coverage of the unit tests, the functional tests
# are optimal.
coverage run --source=debug_toolbar_multilang `which django-admin.py` test -u
# mv .coverage .coverage_unit

# combine and report results 
coverage combine
coverage report
coverage html
