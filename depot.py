import math
from multiDB import TableManager


class Depot:
    def __init__(self, symbol, date):
        self.money = 100000.0
        self.symbol = symbol
        self.printTrade("SELL", 1337, self.symbol, date, 420.69, round(self.money, 2))

    def printTrade(self, action, amount, symbol, date, price, depot):
        print("%5s %4s %4s ON %s FOR %6s | Depot: %10s" % (
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
        self.money += latestTrade[4] * tempTuple[1]
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
