from services import root_dir, json_response
from flask import Flask
import json

app = Flask(__name__)

with open("{}/db/customers.json".format(root_dir()), "r") as f:
    customers = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    amount = len(customers)
    return json_response({
        "uri": "/",
        "customers": f"We have {amount} customers"
    })

if __name__ == '__main__':
    app.run()