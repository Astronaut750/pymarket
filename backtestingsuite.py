from multiDB import TableManager
from depot import Depot
import datetime

stocks = open("stocks.txt").read().split(",")
startingDate = "2015-01-01"

for stock in stocks:
    print("Simulating %s starting at %s\n" % (stock, startingDate))

    tb = TableManager(stock)
    tb.deleteFrom("zz_backtestingsuite")

    date = datetime.date.fromisoformat(startingDate)
    tempTuple = tb.getDataSingleDay(date.isoformat()) # 0 := date | 1 := close | 2 := avg200
    date = datetime.date.fromisoformat(tempTuple[0])

    dpt = Depot(tb.symbol, date)
    splits = tb.getSplits()

    while(date < date.today()):
        try:
            tempTuple = tb.getDataSingleDay(date.isoformat())
        except:
            break

        # Waiting to buy
        while(tempTuple[1] <= tempTuple[2]):
            date += datetime.timedelta(days=1)
            tempTuple = tb.getDataSingleDay(date.isoformat())
            date = datetime.date.fromisoformat(tempTuple[0])

        dpt.addBuyingTrade(tb, tempTuple)

        # Waiting to sell
        while(tempTuple[1] >= tempTuple[2]):
            date += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(date.isoformat())
            except:
                break
            date = datetime.date.fromisoformat(tempTuple[0])

            # Checking for split
            for s in splits:
                if date.isoformat() == s[0]:
                    dpt.addSplitCorrection(tb, tempTuple, s[1])
            
        dpt.addSellingTrade(tb, tempTuple)

    print("\n\n")