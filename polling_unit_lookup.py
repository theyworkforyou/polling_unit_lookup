import re

import requests
from flask import Flask, request, redirect

from polling_unit import tidy_up_pun, pun_re


app = Flask(__name__)

mapit_url_template = 'http://www.shineyoureye.org/mapit/code/poll_unit/{pun}'


@app.route("/")
def polling_unit_lookup():
    query = request.args.get('q')
    pun = tidy_up_pun(query)

    if not pun_re.search(pun):
        return "{} is not a valid polling unit number".format(query)

    return redirect(get_area_from_pun(pun))


def get_area_from_pun(pun):
    while pun:
        try:
            r = requests.get(mapit_url_template.format(pun=pun),
                             allow_redirects=False)
            return r.headers.get('location')
        except requests.exceptions.HTTPError:
            # strip off last component
            pun = re.sub(r'[^:]+$', '', pun)
            pun = re.sub(r':$', '', pun)


if __name__ == "__main__":
    app.run(debug=True)
