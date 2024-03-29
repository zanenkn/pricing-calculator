from services import root_dir, json_response
from flask import Flask, request
from datetime import date, datetime, timedelta
import json
import requests

app = Flask(__name__)

with open("{}/db/customers.json".format(root_dir()), "r") as f:
    customers = json.load(f)

def howManyDays(start, end):
    return (date.fromisoformat(end) - date.fromisoformat(start)).days + 1

def getDates(startDate, endDate):
    dateArray = []
    if endDate == None:
      endDate = (date.today()).isoformat()
    if startDate == None:
      return []
    else:
      currentDate = date.fromisoformat(startDate)
      while currentDate <= date.fromisoformat(endDate):
        dateArray.append(currentDate)
        currentDate = currentDate + timedelta(days=1)
      return dateArray
    
def dropWeekends(rng):
    return [d for d in rng if not d.isoweekday() in [6,7]]
  
def getFirstPaidDay(lastFreeDay):
    if lastFreeDay == None:
      firstPaidDay = None
    else:
      firstPaidDay = lastFreeDay + timedelta(days=1)
    return firstPaidDay

def getPaidServiceStart(startA, endA, startB, endB, startC, endC, startCustomer, free):
    a = getDates(startA, endA)
    aDates = dropWeekends(a)
    b = getDates(startB, endB)
    bDates = dropWeekends(b)
    cDates = getDates(startC, endC)
    currentDay = date.fromisoformat(startCustomer)
    freeDays = free
    today = date.today()
    lastFreeDayA = None
    lastFreeDayB = None
    lastFreeDayC = None
    
    while currentDay < today:
      if currentDay in aDates:
        freeDays -= 1
        lastFreeDayA = currentDay
        if freeDays == 0:
          break
      if currentDay in bDates:
        freeDays -= 1
        lastFreeDayB = currentDay
        if freeDays == 0:
          break
      if currentDay in cDates:
        freeDays -= 1
        lastFreeDayC = currentDay
        if freeDays == 0:
          break
      currentDay += timedelta(days=1)
    
    return [
      {'firstPaidDayA': getFirstPaidDay(lastFreeDayA)},
      {'firstPaidDayB': getFirstPaidDay(lastFreeDayB)},
      {'firstPaidDayC': getFirstPaidDay(lastFreeDayC)}
    ]

def getStart(start1, start2):
    if start1 == None or start2 == None:
      start = None
    elif start1 > start2:
      start = start1
    else:
      start = start2
    return start

def getEnd(end1, end2):
    if end2 == None:
      end2 = date.today()
      
    if end1 == None:
      end = None
    elif end1 > end2:
      end = end2
    else:
      end = end1
    return end

@app.route("/", methods=['GET'])
def hello():
    amount = len(customers)
    return json_response({
        "uri": "/",
        "customers": f"We have {amount} customers"
    })
    
@app.route("/calculate/<id>")
def calculate(id):
  start = date.fromisoformat(request.args.get('start'))
  end = date.fromisoformat(request.args.get('end'))
  
  customer = customers[id]
  free = customers[id]['free_days']
  startCustomer = customers[id]['since']
  
  if customers[id]['a'] == None:
    startA = None
    endA = None
    chargeFullPriceEndA = None
  else:
    startA = customers[id]['a']['start']
    endA = customers[id]['a']['end']
    chargeFullPriceEndA = getEnd(end, date.fromisoformat(endA))
  
  if customers[id]['b'] == None:
    startB = None
    endB = None
    chargeFullPriceEndB = None
  else:
    startB = customers[id]['b']['start']
    endB = customers[id]['b']['end']
    chargeFullPriceEndB = getEnd(end, date.fromisoformat(endB))
    
  if customers[id]['c'] == None:
    startC = None
    endC = None
    chargeFullPriceEndC = None
  else:
    startC = customers[id]['c']['start']
    endC = customers[id]['c']['end']
    chargeFullPriceEndC = getEnd(end, date.fromisoformat(endC))
    
  paidServiceStart = getPaidServiceStart(startA, endA, startB, endB, startC, endC, startCustomer, free)
  paidServiceStartA = (paidServiceStart[0]['firstPaidDayA'])
  paidServiceStartB = (paidServiceStart[1]['firstPaidDayB'])
  paidServiceStartC = (paidServiceStart[2]['firstPaidDayC'])
  
  chargeFullPriceStartA = getStart(start, paidServiceStartA)
  chargeFullPriceStartB = getStart(start, paidServiceStartB)
  chargeFullPriceStartC = getStart(start, paidServiceStartC)
  
  
  if id not in customers:
      raise Exception
      
  return json_response({
      "aStart": f"{chargeFullPriceStartA}",
      "bStart": f"{chargeFullPriceStartB}",
      "cStart": f"{chargeFullPriceStartC}",
      "aEnd": f"{chargeFullPriceEndA}",
      "bEnd": f"{chargeFullPriceEndB}",
      "cEnd": f"{chargeFullPriceEndC}"
  })

if __name__ == '__main__':
    app.run()