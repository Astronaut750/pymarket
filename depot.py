import math
from multiDB import TableManager


class Depot:
    def __init__(self, starting_money, symbol, date, tb):
        self.money = starting_money
        self.symbol = symbol
        self._initiateDepot(date, tb)
        # latestTrade => 0 := date, 1 := ticker, 2 := action, 3 := price, 4 := amount, 5 := depot

    def _initiateDepot(self, date, tb):
        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"SELL\", %s, %s, %s)" % (
            date, self.symbol, 0.0, 0, self.money)
        self.printTrade("SELL", 0, self.symbol, date, 0.0, round(self.money, 2))
        tb.cursor.execute(sql)
        tb.commit()

    def printTrade(self, action, amount, symbol, date, price, depot):
        print("%5s %4s %4s ON %s FOR %7s | Depot: %10s" % (
            action, amount, symbol, date, price, depot))

    def addBuyingTrade(self, tb, tempTuple):
        amount = math.floor(self.money / tempTuple[1])
        self.money = round(self.money - tempTuple[1] * amount, 2)
        self.printTrade("BUY", amount, self.symbol, tempTuple[0], tempTuple[1], self.money)
        
        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"BUY\", %s, %s, %s)" % (
            tempTuple[0], self.symbol, tempTuple[1], amount, self.money)

        tb.cursor.execute(sql)
        tb.commit()

    def addSellingTrade(self, tb, tempTuple):
        latestTrade = tb.getLatestTrade()
        amount = latestTrade[4]
        self.money += amount * tempTuple[1]
        self.money = round(self.money, 2)
        self.printTrade("SELL", latestTrade[4], self.symbol, tempTuple[0], tempTuple[1], self.money)

        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"SELL\", %s, %s, %s)" % (
            tempTuple[0], self.symbol, tempTuple[1], latestTrade[4], self.money)

        tb.cursor.execute(sql)
        tb.commit()

    def addSplitCorrection(self, tb, tempTuple, value):
        latestTrade = tb.getLatestTrade()
        amount = int(latestTrade[4] * value)

        self.printTrade("SPLIT", amount, self.symbol, tempTuple[0], tempTuple[1], self.money)

        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"SPLT\", %s, %s, %s)" % (
            tempTuple[0], self.symbol, latestTrade[3], amount, self.money)
        tb.cursor.execute(sql)
        tb.commit()
