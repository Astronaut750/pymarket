from multiDB import TableManager
from depot import Depot
import datetime

tb = TableManager("tsla")
tb.deleteFrom("zz_backtestingsuite")

date = datetime.date.fromisoformat("2015-01-01")
currentTuple = tb.getDataSingleDay(date.isoformat())
# 0 := date
# 1 := close
# 2 := avg200

date = datetime.date.fromisoformat(currentTuple[0])

dpt = Depot(tb.symbol)

splits = tb.getSplits()

while(date < date.today()):
    try:
        currentTuple = tb.getDataSingleDay(date.isoformat())
    except:
        break
    # Waiting to buy
    while(currentTuple[1] <= currentTuple[2]):
        date += datetime.timedelta(days=1)
        currentTuple = tb.getDataSingleDay(date.isoformat())
        date = datetime.date.fromisoformat(currentTuple[0])
        # print(date.isoformat())

    dpt.addBuyingTrade(currentTuple)

    # Waiting to sell
    while(currentTuple[1] >= currentTuple[2]):
        date += datetime.timedelta(days=1)
        try:
            currentTuple = tb.getDataSingleDay(date.isoformat())
        except:
            break

        date = datetime.date.fromisoformat(currentTuple[0])

        # Checking for split
        for s in splits:
            if date.isoformat() == s[0]:
                dpt.addSplitCorrection(currentTuple, s[1])
        # print(date.isoformat())
    dpt.addSellingTrade(currentTuple)

print(dpt.money)
