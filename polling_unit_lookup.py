import os
import re

import requests
from flask import Flask, jsonify

from polling_unit import tidy_up_pun, pun_re


app = Flask(__name__)
app.config['MAPIT_API_URL'] = os.environ.get(
    'MAPIT_API_URL', 'http://www.shineyoureye.org/mapit')


def mapit_url(pun):
    return '{mapit}/code/poll_unit/{pun}'.format(
        mapit=app.config['MAPIT_API_URL'],
        pun=pun)


def get_area_from_pun(pun):
    while pun:
        r = requests.get(mapit_url(pun))
        if r.status_code == 200:
            return r.json()
        # strip off last component
        pun = re.sub(r'[^:]+$', '', pun)
        pun = re.sub(r':$', '', pun)


@app.route("/lookup/<polling_unit_number>")
def lookup(polling_unit_number):
    pun = tidy_up_pun(polling_unit_number)

    if not pun_re.search(pun):
        error = 'Unrecognized poll_unit: {}.'
        return jsonify(code=404, error=error.format(polling_unit_number)), 404

    return jsonify(get_area_from_pun(pun))


if __name__ == "__main__":
    app.run(debug=True)
