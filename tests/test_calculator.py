import pytest
import datetime
from datetime import date, timedelta


def getDates(startDate, endDate):
    dateArray = []
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