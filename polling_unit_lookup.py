import os
import re

import requests
from flask import Flask, request, jsonify


# These are hardcoded here rather than being introduced into the mapit database
# to avoid having a huge number of duplicated codes in MapIt. As it is largely
# a presentation thing though I don't think it is too big an issue.
state_number_to_letter_mappings = {
    "1": "AB",
    "2": "AD",
    "3": "AK",
    "4": "AN",
    "5": "BA",
    "6": "BY",
    "7": "BE",
    "8": "BO",
    "9": "CR",
    "10": "DE",
    "11": "EB",
    "12": "ED",
    "13": "EK",
    "14": "EN",
    "15": "GO",
    "16": "IM",
    "17": "JI",
    "18": "KD",
    "19": "KN",
    "20": "KT",
    "21": "KE",
    "22": "KO",
    "23": "KW",
    "24": "LA",
    "25": "NA",
    "26": "NI",
    "27": "OG",
    "28": "ON",
    "29": "OS",
    "30": "OY",
    "31": "PL",
    "32": "RI",
    "33": "SO",
    "34": "TA",
    "35": "YO",
    "36": "ZA",
    "37": "FC",
}


def tidy_up_pun(pun):
    """
    Tidy up the query into something that looks like PUNs we are expecting
    """

    if not pun:
        pun = ""

    pun = pun.strip().upper()
    pun = re.sub(r'[^A-Z\d]+', ':', pun)  # separators to ':'
    pun = re.sub(r'^0+', '',  pun)  # trim leading zeros at start of string
    pun = re.sub(r':0+', ':', pun)  # trim leading zeros for each component

    # PUNs starting with a number shoud be converted to start with a state code
    if re.match(r'^\d', pun):
        state_number = pun.split(':')[0]
        state_code = state_number_to_letter_mappings.get(state_number,
                                                         state_number)
        pun = re.sub(r'^' + state_number, state_code, pun)

    return pun

# A regular expression to match any PUN after it's been tidied
pun_re = re.compile('''
    ^(
       [A-Z]{2}|
       [A-Z]{2}:\d+|
       [A-Z]{2}:\d+:\d+|
       [A-Z]{2}:\d+:\d+:\d+
    )$
''', re.VERBOSE)


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
            return r.json()


@app.route("/")
def lookup():
    polling_unit_number = request.args.get('lookup')
    pun = tidy_up_pun(polling_unit_number)

    if not pun_re.search(pun):
        error = 'Unrecognized polling unit: {}.'
        return jsonify(code=404, error=error.format(polling_unit_number)), 404

    area = get_area_from_pun(pun)

    if not area:
        error = 'No areas were found that matched polling unit: {}'
        return jsonify(code=404, error=error.format(polling_unit_number)), 404

    return jsonify(area)


if __name__ == "__main__":
    app.run(debug=True)
