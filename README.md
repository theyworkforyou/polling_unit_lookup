# Polling Unit Lookup [![Build Status](https://travis-ci.org/theyworkforyou/polling_unit_lookup.svg?branch=master)](https://travis-ci.org/theyworkforyou/polling_unit_lookup)

If you have a [MapIt](http://mapit.poplus.org/) instance which contains Polling Unit codes then you can map between those and MapIt areas using this tool.

## Install

Clone the source code from GitHub and then install the dependencies with `pip`. You might want to create a `virtualenv` or similar to isolate the apps dependencies from the system python packages.

    git clone https://github.com/theyworkforyou/polling_unit_lookup
    cd polling_unit_lookup
    pip install -r requirements.txt

## Usage

    python polling_unit_lookup.py

Then the app will be running at <http://localhost:5000>.
