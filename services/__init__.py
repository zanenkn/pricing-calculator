import os
import json
from flask import make_response


def root_dir():
    return os.path.dirname(os.path.realpath(__file__ + '/..'))


def json_response(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response