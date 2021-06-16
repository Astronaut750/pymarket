from multiDB import TableManager
from depot import Depot
import datetime
import json
import operator as op

# tuple => 0 := date | 1 := close  | 2 := avg200
# trade => 0 := date | 1 := ticker | 2 := action | 3 := price | 4 := amount | 5 := depot

starting_conf = json.loads(open("config.json").read())
starting_conf["starting_money"] /= len(starting_conf["stocks"])

operatorlookup = {
    '>=': op.ge,
    '<=': op.le
}


def strategy200(tb, dpt, tempDate, percent=0, schulerer=False, text="Avg200-Strategy:"):
    while(True):
        try:
            tempTuple = tb.getDataSingleDay(tempDate.isoformat())
        except:
            break

        # Waiting to buy  if not schulerer else op.gt(close, avg200) op.lt(
        while((tempTuple[1] < tempTuple[2] * (1 + 0.01 * percent)
               ) if not schulerer else tempTuple[1] > tempTuple[2] * (1 + 0.01 * percent)):
            tempDate += datetime.timedelta(days=1)
            try:
                tempTuple = tb.getDataSingleDay(tempDate.isoformat())
            except:
                break
            tempDate = datetime.date.fromisoformat(tempTuple[0])

        dpt.addBuyingTrade(tb, tempTuple)

        # Waiting to sell  if not schulerer else op.ge(close, avg200) op.le(
        while((tempTuple[1] >= tempTuple[2] * (1 + 0.01 * percent)
               ) if not schulerer else tempTuple[1] <= tempTuple[2] * (1 + 0.01 * percent)):
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

    # printResult(dpt, text)


def buyAndHold(tb, dpt, tempDate):
    tempTuple = tb.getDataSingleDay(tempDate.isoformat())
    dpt.addBuyingTrade(tb, tempTuple)

    tempTuple = tb.getDataSingleDayBefore(datetime.date.today().isoformat())
    dpt.addSellingTrade(tb, tempTuple)

    # printResult(dpt, "Buy&Hold-Strategy:")


def printLatestTrade(tb, dpt):
    if(starting_conf["print_intertrades"] == False):
        latestTrade = tb.getLatestTrade()
        tempTuple = tb.getDataSingleDay(latestTrade[0])
        dpt.printTrade("SELL", latestTrade[4], tb.getSymbol(
        ), tempTuple[0], tempTuple[1], dpt.getMoney())
        change = round(
            (dpt.getMoney() * 100 / starting_conf["starting_money"]) - 100, 3)

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


def printResult(dpt, text):
    change = round(
        (dpt.getMoney() * 100 / starting_conf["starting_money"]) - 100, 3)
    if change < 0:
        change -= 2 * change
        print("%27s %11s (-%6s%%)" % (text, dpt.getMoney(), change))
        # print("Prozentuale Veränderung: -%6s%%" % change)
    else:
        print("%27s %11s (+%6s%%)" % (text, dpt.getMoney(), change))
        # print("Prozentuale Veränderung: +%6s%%" % change)


strategy200Result = 0.0
strategy200lateResult = 0.0
buyAndHoldResult = 0.0
schulererResult = 0.0

for stock in starting_conf["stocks"]:
    tb = TableManager(stock)

    tempDate = getFirstValidDate()
    print("Simulating %s starting at %s" % (stock, tempDate))

    dpt = Depot(tb.symbol, tb)
    strategy200(tb, dpt, tempDate)
    strategy200Result += dpt.getMoney()

    dpt = Depot(tb.symbol, tb)
    strategy200(tb, dpt, tempDate, percent=3,
                text="Avg200-Strategy (3% late):")
    strategy200lateResult += dpt.getMoney()

    dpt = Depot(tb.symbol, tb)
    buyAndHold(tb, dpt, tempDate)
    buyAndHoldResult += dpt.getMoney()

    dpt = Depot(tb.symbol, tb)
    strategy200(tb, dpt, tempDate, schulerer=True, text="Schulerer-Strategy:")
    schulererResult += dpt.getMoney()


def printResult(strategyResult):
    change = round( (strategyResult * 100 / starting_conf["starting_money"] * len(starting_conf["stocks"])) - 100, 3)
    if change < 0:
        change -= 2 * change
        print("%11s (-%6s%%)" % (strategyResult, change))
    else:
        print("%11s (+%6s%%)" % (strategyResult, change))
    pass

printResult(strategy200Result)
printResult(strategy200lateResult)
printResult(buyAndHoldResult)
printResult(schulererResult)