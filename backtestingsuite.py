from multiDB import TableManager
from depot import Depot
import datetime
import json

starting_conf = json.loads(open("config.json").read())

def strategy200(tb, dpt, tempDate, percent=0):
    while(True):
        try:
            tempTuple = tb.getDataSingleDay(tempDate.isoformat())
        except:
            # print(tempDate.isoformat(), dpt.getMoney())
            break

        # Waiting to buy
        while(tempTuple[1] <= tempTuple[2] * (1 + 0.01 * percent)):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

        dpt.addBuyingTrade(tb, tempTuple)

        # Waiting to sell
        while(tempTuple[1] >= tempTuple[2] * (1 - 0.01 * percent)):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

            # ! unnötig, wenn man die korrigierten Werte vor dem Split nimmt
            # Checking for split
            # for s in splits:
            #    if tempDate.isoformat() == s[0]:
            #        dpt.addSplitCorrection(tb, tempTuple, s[1])

        dpt.addSellingTrade(tb, tempTuple)

    printLatestTrade(tb, dpt)

def schulerer(tb, dpt, tempDate):
    while(True):
        try:
            tempTuple = tb.getDataSingleDay(tempDate.isoformat())
        except:
            # print(tempDate.isoformat(), dpt.getMoney())
            break

        # Waiting to buy
        while(tempTuple[1] >= tempTuple[2]):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

        dpt.addBuyingTrade(tb, tempTuple)

        # Waiting to sell
        while(tempTuple[1] <= tempTuple[2]):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

        dpt.addSellingTrade(tb, tempTuple)

    printLatestTrade(tb, dpt)

def buyAndHold(tb, dpt, tempDate):
    tempTuple = tb.getDataSingleDay(tempDate.isoformat())
    dpt.addBuyingTrade(tb, tempTuple)

    tempTuple = tb.getDataSingleDayBefore(datetime.date.today().isoformat())
    dpt.addSellingTrade(tb, tempTuple)

    printLatestTrade(tb, dpt)

def printLatestTrade(tb, dpt):
    latestTrade = tb.getLatestTrade()
    tempTuple = tb.getDataSingleDay(latestTrade[0])
    dpt.printTrade("SELL", latestTrade[4], tb.getSymbol(), tempTuple[0], tempTuple[1], dpt.getMoney())
    change = round( (dpt.getMoney() * 100 / starting_conf["starting_money"]) - 100, 1)

    if change < 0:
        change -= 2 * change
        print("Prozentuale Veränderung: -%6s%%" % change)
    else:
        print("Prozentuale Veränderung: +%6s%%" % change)

    print()

def getFirstValidDate():
    date = starting_conf["starting_date"]
    tempTuple = tb.getDataSingleDay(date)
    return datetime.date.fromisoformat(tempTuple[0])


for stock in starting_conf["stocks"]:
    tb = TableManager(stock)
    
    # ignoring splits because we already calculate with adjusted close values
    # splits = tb.getSplits() if starting_conf["with_splits"] else []

    tempDate = getFirstValidDate()
    print("Simulating %s starting at %s\n" % (stock, tempDate))

    print("Avg200-Strategy:")
    dpt = Depot(tb.symbol, tb)
    strategy200(tb, dpt, tempDate)

    print("Avg200-Strategy (3% late):")
    dpt = Depot(tb.symbol, tb)
    strategy200(tb, dpt, tempDate, percent=3)

    print("Buy&Hold-Strategy:")
    dpt = Depot(tb.symbol, tb)
    buyAndHold(tb, dpt, tempDate)

    print("Schulerer-Strategy:")
    dpt = Depot(tb.symbol, tb)
    schulerer(tb, dpt, tempDate)

    print("\n\n")

    # tuple => 0 := date | 1 := close  | 2 := avg200
    # trade => 0 := date | 1 := ticker | 2 := action | 3 := price | 4 := amount | 5 := depot