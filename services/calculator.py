from services import root_dir, json_response
from flask import Flask, request
from datetime import date, datetime, timedelta
import json

app = Flask(__name__)

with open("{}/db/customers.json".format(root_dir()), "r") as f:
    customers = json.load(f)

def how_many(start, end):
    return date.fromisoformat(end) - date.fromisoformat(start)

def getDates(startDate, endDate):
    dateArray = []
    currentDate = date.fromisoformat(startDate)
    while currentDate <= date.fromisoformat(endDate):
      dateArray.append(currentDate)
      currentDate = currentDate + timedelta(days=1)
    return dateArray

@app.route("/", methods=['GET'])
def hello():
    amount = len(customers)
    return json_response({
        "uri": "/",
        "customers": f"We have {amount} customers"
    })
    
@app.route("/calculate/<id>")
def calculate(id):
  start=request.args.get('start')
  end=request.args.get('end')
  
  if id not in customers:
      raise Exception
      
  return json_response({
      "days": f"{how_many(start, end).days + 1}",
      "dates": f"{getDates(start, end)}"
  })

if __name__ == '__main__':
    app.run()