import mysql.connector


def open():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pymarket"
    )


class TableManager:
    conn = None
    cursor = None
    symbol = ""

    def __init__(self, symbol):
        self.conn = open()
        self.cursor = self.conn.cursor()
        self.symbol = symbol

    def getSymbol(self):
        return self.symbol

    def createTable(self):
        sql = "CREATE TABLE IF NOT EXISTS %s (date CHAR(10) PRIMARY KEY, close REAL, average200 REAL);" % self.symbol
        self.cursor.execute(sql)

    def insertClose(self, date, close):
        sql = "INSERT INTO %s (date, close) VALUES (\"%s\", %s);" % (
            self.symbol, date, close)
        self.cursor.execute(sql)

    def insertAverage200(self, date, average200):
        sql = "UPDATE %s SET average200 = %s WHERE date = \"%s\";" % (
            self.symbol, average200, date)
        self.cursor.execute(sql)

    def insertSaisonal(self, symbol, year, month, gain):
        sql = "INSERT INTO zz_saisonal_m VALUES(\"%s\", %s, %s, %s);" % (
            symbol, year, month, gain)
        self.cursor.execute(sql)

    def insertSplit(self, date, value):
        sql = "INSERT INTO zz_splits values (\"%s\", \"%s\", %s)" % (
            self.symbol, date, value)
        self.cursor.execute(sql)

    def deleteFromSaisonal(self):
        sql = "DELETE FROM zz_saisonal_m;"
        self.cursor.execute(sql)
        self.commit()

    def getLatestTrade(self):
        sql = "SELECT * FROM zz_backtestingsuite order by date desc limit 1"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def getSplits(self):
        sql = "SELECT date, value FROM zz_splits WHERE ticker = \"%s\"" % self.symbol
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def deleteFrom(self, symbol):
        sql = "DELETE FROM %s;" % symbol
        self.cursor.execute(sql)
        self.commit()

    def deleteSplits(self):
        sql = "DELETE FROM zz_splits where ticker = \"%s\"" % self.symbol
        self.cursor.execute(sql)
        self.commit()

    def commit(self):
        self.conn.commit()

    def getTableSize(self):
        sql = "SELECT count(date) FROM %s;" % self.symbol
        self.cursor.execute(sql)
        return int(self.cursor.fetchone()[0])

    def getLatestDate(self):
        sql = "SELECT date FROM %s ORDER BY date DESC LIMIT 1;" % self.symbol
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def getFirstDate(self):
        sql = "SELECT date FROM %s ORDER BY date ASC LIMIT 1;" % self.symbol
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def getFirstAVG200Date(self):
        sql = "SELECT date FROM %s WHERE average200 IS NOT NULL ORDER BY date ASC LIMIT 1;" % self.symbol
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def getAllData(self):
        sql = "SELECT * FROM %s ORDER BY date DESC;" % self.symbol
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getAllDataForPlot(self):
        sql = "SELECT * FROM %s WHERE average200 IS NOT NULL ORDER BY DATE ASC;" % self.symbol
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getSpecDataForPlot(self, begDate, endDate):
        sql = "SELECT * FROM %s WHERE average200 IS NOT NULL AND date >= \"%s\" AND date <= \"%s\" ORDER BY DATE ASC;" % (
            self.symbol, begDate, endDate)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getDataForRanking(self, month, year):
        begMonth = year + "-" + month.zfill(2) + "-01"
        endMonth = year + "-" + month.zfill(2) + "-31"
        sql = "SELECT * FROM %s WHERE date >= \"%s\" AND date <= \"%s\" ORDER BY DATE ASC;" % (
            self.symbol, begMonth, endMonth)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getDataSingleDay(self, date):
        sql = "SELECT * FROM %s WHERE date >= \"%s\" LIMIT 1" % (
            self.symbol, date)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def getDataSingleDayBefore(self, date):
        sql = "SELECT * FROM %s WHERE date <= \"%s\" ORDER BY date DESC LIMIT 1" % (
            self.symbol, date)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def getGainsForMonth(self, month):
        sql = "SELECT * FROM zz_saisonal_m WHERE month = %s AND stockTicker = \"%s\";" % (
            month, self.symbol)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getGainForMonth(self, month):
        sql = "SELECT * FROM %s WHERE month = %s" % (self.symbol, month)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def isLatestCloseAboveAverage200(self):
        latestDate = self.getLatestDate()
        sql = "SELECT close, average200 FROM %s WHERE date = \"%s\";" % (
            self.symbol, latestDate)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return float(result[0]) > float(result[1])

    def dropTable(self):
        sql = "DROP TABLE %s;" % self.symbol
        self.cursor.execute(sql)
