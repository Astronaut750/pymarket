import math
from multiDB import TableManager


class Depot:
    money = 0.0
    trades = []
    symbol = ""

    def __init__(self, symbol):
        self.money = 100000.0
        self.symbol = symbol

    def addBuyingTrade(self, data):
        amount = math.floor(self.money / data[1])
        self.money = round(self.money - data[1] * amount, 2)
        print("  BUY", amount, self.symbol, "ON",
              data[0], "FOR", data[1], "| Depot:", self.money)
        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"BUY\", %s, %s, %s)" % (
            data[0], self.symbol, data[1], amount, self.money)

        tb = TableManager(self.symbol)
        tb.cursor.execute(sql)
        tb.commit()

    def addSellingTrade(self, data):
        tb = TableManager(self.symbol)
        latestTrade = tb.getLatestTrade()
        self.money += round(latestTrade[4] * data[1], 2)
        print(" SELL", latestTrade[4], self.symbol, "ON",
              data[0], "FOR", data[1], "| Depot:", self.money)

        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"SELL\", %s, %s, %s)" % (
            data[0], self.symbol, data[1], latestTrade[4], self.money)

        tb.cursor.execute(sql)
        tb.commit()

    def addSplitCorrection(self, data, value):
        tb = TableManager(self.symbol)
        latestTrade = tb.getLatestTrade()
        amount = latestTrade[4] * value
        print("SPLIT", amount, self.symbol, "ON",
              data[0], "FOR", latestTrade[3], "| Depot:", self.money)

        sql = "insert into zz_backtestingsuite values (\"%s\", \"%s\", \"SPLT\", %s, %s, %s)" % (
            data[0], self.symbol, latestTrade[3], amount, self.money)
        tb.cursor.execute(sql)
        tb.commit()
