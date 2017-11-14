import fileinput
import importlib

import sys
import flask
from piecash_utilities import execute_report

app = flask.Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    print(flask.request.data)
    print(flask.request.headers)
    return flask.Response("<html><body>ok all</body></html>",
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

