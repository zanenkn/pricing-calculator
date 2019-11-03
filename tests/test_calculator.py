import pytest
import datetime
from datetime import date, timedelta


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
  
def test_getDates():
    assert getDates('2019-10-01', '2019-10-10') == [datetime.date(2019, 10, 1), datetime.date(2019, 10, 2), datetime.date(2019, 10, 3), datetime.date(2019, 10, 4), datetime.date(2019, 10, 5), datetime.date(2019, 10, 6), datetime.date(2019, 10, 7), datetime.date(2019, 10, 8), datetime.date(2019, 10, 9), datetime.date(2019, 10, 10)]
    
def dropWeekends(rng):
    return [d for d in rng if not d.isoweekday() in [6,7]]

def test_dropWeekends():
    rng = [datetime.date(2019, 10, 1), datetime.date(2019, 10, 2), datetime.date(2019, 10, 3), datetime.date(2019, 10, 4), datetime.date(2019, 10, 5), datetime.date(2019, 10, 6), datetime.date(2019, 10, 7), datetime.date(2019, 10, 8), datetime.date(2019, 10, 9), datetime.date(2019, 10, 10)]
    assert dropWeekends(rng) == [datetime.date(2019, 10, 1), datetime.date(2019, 10, 2), datetime.date(2019, 10, 3), datetime.date(2019, 10, 4), datetime.date(2019, 10, 7), datetime.date(2019, 10, 8), datetime.date(2019, 10, 9), datetime.date(2019, 10, 10)]
    
def getFreeServiceEnd(startA, endA, startB, endB, startC, endC, startCustomer, free):
    a = getDates(startA, endA)
    aDates = dropWeekends(a)
    b = getDates(startB, endB)
    bDates = dropWeekends(b)
    cDates = getDates(startC, endC)
    currentDay = startCustomer
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
      currentDay += + timedelta(days=1)
    return [
      {'last_a': lastFreeDayA},
      {'last_b': lastFreeDayB},
      {'last_c': lastFreeDayC}
    ]

def test_1getFreeServiceEnd():
    startA = '2019-10-01'
    endA =  '2019-10-10'
    startB = '2019-10-05'
    endB = '2019-10-10'
    startC = '2019-10-08'
    endC = '2019-10-10'
    startCustomer = datetime.date(2019, 9, 9)
    free = 8
    assert getFreeServiceEnd(startA, endA, startB, endB, startC, endC, startCustomer, free) == [{'last_a': datetime.date(2019, 10, 8)}, {'last_b': datetime.date(2019, 10, 8)}, {'last_c': None}]

def test_2getFreeServiceEnd():
    startA = '2019-10-01'
    endA =  '2019-10-10'
    startB = '2019-10-05'
    endB = '2019-10-10'
    startC = None
    endC = None
    startCustomer = datetime.date(2019, 9, 9)
    free = 8
    assert getFreeServiceEnd(startA, endA, startB, endB, startC, endC, startCustomer, free) == [{'last_a': datetime.date(2019, 10, 8)}, {'last_b': datetime.date(2019, 10, 8)}, {'last_c': None}]
    
def test_3getFreeServiceEnd():
    startA = '2019-10-01'
    endA =  '2019-10-10'
    startB = '2019-10-05'
    endB = None
    startC = None
    endC = None
    startCustomer = datetime.date(2019, 9, 9)
    free = 8
    assert getFreeServiceEnd(startA, endA, startB, endB, startC, endC, startCustomer, free) == [{'last_a': datetime.date(2019, 10, 8)}, {'last_b': datetime.date(2019, 10, 8)}, {'last_c': None}]
    