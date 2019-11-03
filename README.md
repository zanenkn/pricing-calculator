# Plan

1. Find out the last free day for a, b and c

2. For each service compare the last free day with start param sent in
```
param > last free day  - chargeFullPriceStartDate is the param
```
```
param < last free day - chargeFullPriceStartDate is next day after the last free
```

3. For each service compare the service end day with end param sent in
```
if service end day is null then service end day is today
```
```
param > service end day - chargeFullPriceEndDate is service end day
```
```
param < service end day - chargeFullPriceEndDate is param
```

4. For each service if there is a discount
```
if discount start date > chargeFullPriceStartDate - chargeDiscountedPriceStartDate is discount start date
```
```
if discount start date < chargeFullPriceStartDate - chargeDiscountedPriceStartDate is chargeFullPriceStartDate
```
```
if discount end date > chargeFullPriceEndDate - chargeDiscountedPriceEndDate is chargeFullPriceEndDate
```
```
if discount end date < chargeFullPriceEndDate - chargeDiscountedPriceEndDate is if discount end date
```

5. For each service find out how many days between
```  
chargeDiscountedPriceStartDate and chargeDiscountedPriceEndDate (drop Saturdays and Sundays for services a and b)
```
```
chargeFullPriceStartDate and chargeFullPriceEndDate (drop Saturdays and Sundays for services a and b)
```
		
first  = discountedDays
fullPriceDays = second - discountedDays

6. For each service
```
if price override is not null then price is price override, else price is the base price
```
```
total = discountedDays * (price * discount) + fullPriceDays * price
```

7. Sum totals for all services and return