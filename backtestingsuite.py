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


def schulerer(tb, dpt, tempDate, percent=0):
    while(True):
        try:
            tempTuple = tb.getDataSingleDay(tempDate.isoformat())
        except:
            # print(tempDate.isoformat(), dpt.getMoney())
            break

        # Waiting to buy
        while(tempTuple[1] >= tempTuple[2] * (1 + 0.01 * percent)):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

        dpt.addBuyingTrade(tb, tempTuple)

        # Waiting to sell
        while(tempTuple[1] <= tempTuple[2] * (1 - 0.01 * percent)):
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


def buyAndHold(tb, dpt, tempDate):
    tempTuple = tb.getDataSingleDay(tempDate.isoformat())
    dpt.addBuyingTrade(tb, tempTuple)

    tempTuple = tb.getDataSingleDayBefore(datetime.date.today().isoformat())
    dpt.addSellingTrade(tb, tempTuple)


for stock in starting_conf["stocks"]:
    tb = TableManager(stock)
    splits = [] if starting_conf["with_splits"] == False else tb.getSplits()
    tb.deleteFrom("zz_backtestingsuite")

    # Getting date from config as str
    tempDate = starting_conf["starting_date"]

    # getting temporary first tuple
    tempTuple = tb.getDataSingleDay(tempDate)
    # tempTuple => 0 := date | 1 := close | 2 := avg200

    tempDate = datetime.date.fromisoformat(tempTuple[0])

    print("Simulating %s starting at %s" % (stock, tempDate))

    print("Avg200-Strategy:")
    tb.deleteFrom("zz_backtestingsuite")
    dpt = Depot(starting_conf["starting_money"],
                tb.symbol, starting_conf["starting_date"], tb)
    strategy200(tb, dpt, tempDate)

    print()

    print("Avg200-Strategy (3% late):")
    tb.deleteFrom("zz_backtestingsuite")
    dpt = Depot(starting_conf["starting_money"],
                tb.symbol, starting_conf["starting_date"], tb)
    strategy200(tb, dpt, tempDate, percent=3)

    print()

    print("Buy&Hold-Strategy:")
    tb.deleteFrom("zz_backtestingsuite")
    dpt = Depot(starting_conf["starting_money"],
                tb.symbol, starting_conf["starting_date"], tb)
    buyAndHold(tb, dpt, tempDate)

    print()

    print("Schulerer-Strategy:")
    tb.deleteFrom("zz_backtestingsuite")
    dpt = Depot(starting_conf["starting_money"],
                tb.symbol, starting_conf["starting_date"], tb)
    schulerer(tb, dpt, tempDate)

    # print(tb.getDataSingleDayBefore(datetime.date.today().isoformat()))
