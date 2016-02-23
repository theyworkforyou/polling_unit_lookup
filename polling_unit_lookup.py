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
    variations = [pun.rsplit(':', n)[0] for n in range(0, len(pun.split(':')))]
    for pun_variation in variations:
        r = requests.get(mapit_url(pun_variation))
        if r.status_code == 200:
            return jsonify(r.json())


@app.route("/lookup/<polling_unit_number>")
def lookup(polling_unit_number):
    pun = tidy_up_pun(polling_unit_number)

    if not pun_re.search(pun):
        error = 'Unrecognized polling unit: {}.'
        return jsonify(code=404, error=error.format(polling_unit_number)), 404

    area = get_area_from_pun(pun)

    if not area:
        error = 'No areas were found that matched polling unit: {}'
        return jsonify(code=404, error=error.format(polling_unit_number)), 404

    return area


if __name__ == "__main__":
    app.run(debug=True)
