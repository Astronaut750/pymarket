from json.decoder import JSONDecoder
from multiDB import TableManager
from depot import Depot
import datetime
import json

stocks = open("stocks.txt").read().split(",")
starting_conf = json.loads(open("backtestingsuite.json").read())

for stock in stocks:
    tb = TableManager(stock)
    
    splits = [] if starting_conf["with_splits"] == False else tb.getSplits()

    tb.deleteFrom("zz_backtestingsuite")

    # Getting date from config as str
    tempDate = starting_conf["starting_date"]

    # getting temporary first tuple
    tempTuple = tb.getDataSingleDay(tempDate)
    # tempTuple => 0 := date | 1 := close | 2 := avg200

    # 
    tempDate = datetime.date.fromisoformat(tempTuple[0])

    print("\nSimulating %s starting at %s\n" % (stock, tempDate))
    dpt = Depot(starting_conf["starting_money"], tb.symbol, tempDate, tb)

    #tempDate < datetime.date.today()
    while(True):
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

    print("\n")