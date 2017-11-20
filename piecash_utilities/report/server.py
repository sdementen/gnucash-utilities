import fileinput
import importlib

import sys
import flask
from piecash_utilities import execute_report

app = flask.Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    print(flask.request.data.decode("UTF-8"))
    print(flask.request.headers)
    report = flask.request.headers["Gnc-Report"]
    inputs = flask.request.data.decode("UTF-8").split("\n")
    sys.path.append(inputs[1])
    mod = importlib.import_module("{report}.{report}".format(report=report))
    res = mod.generate_report(inputs[0], inputs[2:])

    return flask.Response(res,
                       mimetype='text/html'   )
app.run(debug=True, port=8001)
fdfdsfds

inputs = sys.stdin.readlines()
module = inputs[0]
book = inputs[1]
rest = inputs[2:]
print(module)

mod = importlib.import_module(module)

try:
    res = execute_report(mod.generate_report, book)
except:
    print("ko")
sys.exit()

