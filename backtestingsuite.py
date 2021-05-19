from multiDB import TableManager
from depot import Depot
import datetime

stocks = open("stocks.txt").read().split(",")
tempDate = "2015-01-01"

for stock in stocks:
    print("Simulating %s starting at %s\n" % (stock, tempDate))

    tb = TableManager(stock)
    tb.deleteFrom("zz_backtestingsuite")

    tempDate = datetime.date.fromisoformat(tempDate)
    tempTuple = tb.getDataSingleDay(tempDate.isoformat()) # 0 := date | 1 := close | 2 := avg200
    tempDate = datetime.date.fromisoformat(tempTuple[0])

    dpt = Depot(tb.symbol, tempDate)
    splits = tb.getSplits()

    while(tempDate < datetime.date.today()):
        try:
            tempTuple = tb.getDataSingleDay(tempDate.isoformat())
        except:
            break

        # Waiting to buy
        while(tempTuple[1] <= tempTuple[2]):
            tempDate += datetime.timedelta(days=1)
            tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            tempDate = datetime.date.fromisoformat(tempTuple[0])

        dpt.addBuyingTrade(tb, tempTuple)

        # Waiting to sell
        while(tempTuple[1] >= tempTuple[2]):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

            # Checking for split
            for s in splits:
                if tempDate.isoformat() == s[0]:
                    dpt.addSplitCorrection(tb, tempTuple, s[1])
            
        dpt.addSellingTrade(tb, tempTuple)
    
    print("\n\n")