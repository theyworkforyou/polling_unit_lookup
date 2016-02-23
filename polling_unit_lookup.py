from flask import Flask, request
from polling_unit import tidy_up_pun, pun_re


app = Flask(__name__)


@app.route("/")
def polling_unit_lookup():
    pun = tidy_up_pun(request.args.get('q'))
    if pun_re.search(pun):
        return "{} is a valid polling unit number".format(pun)
    else:
        return "{} is not a valid polling unit number".format(pun)

if __name__ == "__main__":
    app.run(debug=True)
