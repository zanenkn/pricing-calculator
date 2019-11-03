import pytest
import datetime
from datetime import date, timedelta

# function to get an array of dates between 2
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
    expected = [
      datetime.date(2019, 10, 1), 
      datetime.date(2019, 10, 2), 
      datetime.date(2019, 10, 3), 
      datetime.date(2019, 10, 4), 
      datetime.date(2019, 10, 5), 
      datetime.date(2019, 10, 6), 
      datetime.date(2019, 10, 7), 
      datetime.date(2019, 10, 8), 
      datetime.date(2019, 10, 9), 
      datetime.date(2019, 10, 10)
    ]
    
    assert getDates('2019-10-01', '2019-10-10') == expected


# function to remove saturdays and sundays from an array of dates    
def dropWeekends(rng):
    return [d for d in rng if not d.isoweekday() in [6,7]]

def test_dropWeekends():
    rng = [
      datetime.date(2019, 10, 1), 
      datetime.date(2019, 10, 2), 
      datetime.date(2019, 10, 3), 
      datetime.date(2019, 10, 4), 
      datetime.date(2019, 10, 5), 
      datetime.date(2019, 10, 6), 
      datetime.date(2019, 10, 7), 
      datetime.date(2019, 10, 8), 
      datetime.date(2019, 10, 9), 
      datetime.date(2019, 10, 10)
    ]
    
    expected = [
      datetime.date(2019, 10, 1), 
      datetime.date(2019, 10, 2), 
      datetime.date(2019, 10, 3), 
      datetime.date(2019, 10, 4), 
      datetime.date(2019, 10, 7), 
      datetime.date(2019, 10, 8), 
      datetime.date(2019, 10, 9), 
      datetime.date(2019, 10, 10)
    ]
    
    assert dropWeekends(rng) == expected


# function to get a first paid day out of the last free day
def getFirstPaidDay(lastFreeDay):
    if lastFreeDay == None:
      firstPaidDay = None
    else:
      firstPaidDay = lastFreeDay + timedelta(days=1)
    return firstPaidDay

# function to determine on what date to start charging for services A, B and C considering the free days        
def getPaidServiceStart(startA, endA, startB, endB, startC, endC, startCustomer, free):
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
      currentDay += timedelta(days=1)
    
    return [
      {'firstPaidDayA': getFirstPaidDay(lastFreeDayA)},
      {'firstPaidDayB': getFirstPaidDay(lastFreeDayB)},
      {'firstPaidDayC': getFirstPaidDay(lastFreeDayC)}
    ]

def test_1getPaidServiceStart():
    startA = '2019-10-01'
    endA =  '2019-10-10'
    startB = '2019-10-05'
    endB = '2019-10-10'
    startC = '2019-10-08'
    endC = '2019-10-10'
    startCustomer = datetime.date(2019, 9, 9)
    free = 8
    
    expected = [
      {'firstPaidDayA': datetime.date(2019, 10, 9)}, 
      {'firstPaidDayB': datetime.date(2019, 10, 9)}, 
      {'firstPaidDayC': None}]
    
    assert getPaidServiceStart(startA, endA, startB, endB, startC, endC, startCustomer, free) == expected

def test_2getPaidServiceStart():
    startA = '2019-10-01'
    endA =  '2019-10-10'
    startB = '2019-10-05'
    endB = '2019-10-10'
    startC = None
    endC = None
    startCustomer = datetime.date(2019, 9, 9)
    free = 8
    
    expected = [
      {'firstPaidDayA': datetime.date(2019, 10, 9)}, 
      {'firstPaidDayB': datetime.date(2019, 10, 9)}, 
      {'firstPaidDayC': None}
    ]
    
    assert getPaidServiceStart(startA, endA, startB, endB, startC, endC, startCustomer, free) == expected
    
def test_3getPaidServiceStart():
    startA = '2019-10-01'
    endA =  '2019-10-10'
    startB = '2019-10-05'
    endB = None
    startC = None
    endC = None
    startCustomer = datetime.date(2019, 9, 9)
    free = 8
    
    expected = [
      {'firstPaidDayA': datetime.date(2019, 10, 9)}, 
      {'firstPaidDayB': datetime.date(2019, 10, 9)}, 
      {'firstPaidDayC': None}
    ]
    
    assert getPaidServiceStart(startA, endA, startB, endB, startC, endC, startCustomer, free) == expected


# function that determines the start date of full price service (param, firstPaidDay) / start date of discounted service (discountStart, firstPaidDay)   
def getStart(start1, start2):
    if start1 > start2:
      start = start1
    else:
      start = start2
    return start

def getStart():
    assert getStart(datetime.date(2019, 9, 9), datetime.date(2019, 10, 1)) == datetime.date(2019, 10, 2)
    
def getStart():
    assert getStart(datetime.date(2019, 9, 9), datetime.date(2019, 8, 29)) == datetime.date(2019, 9, 9)
 
    
# function that determines the end date of full price service      
def getChargeFullPriceEndDate(paramEnd, serviceEnd):
    if serviceEnd == None:
      serviceEnd = date.today()
    if paramEnd > serviceEnd:
      chargeFullPriceEndDate = serviceEnd
    else:
      chargeFullPriceEndDate = paramEnd
    return chargeFullPriceEndDate
  
def test_1getChargeFullPriceEndDate():
    assert getChargeFullPriceEndDate(datetime.date(2019, 9, 9), datetime.date(2019, 10, 1)) == datetime.date(2019, 9, 9)
    
def test_2getChargeFullPriceEndDate():
    assert getChargeFullPriceEndDate(datetime.date(2019, 10, 10), datetime.date(2019, 9, 18)) == datetime.date(2019, 9, 18)
    
def test_3getChargeFullPriceEndDate():
    assert getChargeFullPriceEndDate(datetime.date(2019, 10, 10), None) == datetime.date(2019, 10, 10)
