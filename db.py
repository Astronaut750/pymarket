import mysql.connector


def open():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pymarket"
    )
    return conn


def createTable(cursor, symbol):
    sql = "CREATE TABLE IF NOT EXISTS %s (date char(10) PRIMARY KEY, close real, average200 real)" % symbol
    cursor.execute(sql)


def insertClose(cursor, symbol, day, close):
    sql = "INSERT INTO %s (date, close) VALUES(\"%s\", %s)" % (
        symbol, day, close)
    cursor.execute(sql)


def insertAverage200(cursor, symbol, average200, date):
    sql = "UPDATE %s SET average200 = %s WHERE date = \"%s\"" % (
        symbol, average200, date)
    cursor.execute(sql)


def getTableSize(cursor, symbol):
    sql = "SELECT date FROM %s" % symbol
    cursor.execute(sql)
    result = cursor.fetchall()
    return len(result)


def getLatestDate(cursor, symbol):
    sql = "SELECT date FROM %s ORDER BY date DESC LIMIT 1" % symbol
    cursor.execute(sql)
    return cursor.fetchone()[0]


def getFirstDate(cursor, symbol):
    sql = "SELECT date FROM %s ORDER BY date ASC LIMIT 1" % symbol
    cursor.execute(sql)
    return cursor.fetchone()[0]


def getAllData(cursor, symbol):
    sql = "SELECT * FROM %s ORDER BY date DESC" % symbol
    cursor.execute(sql)
    return cursor.fetchall()


def getAllDataForPlot(cursor, symbol):
    sql = "SELECT * FROM %s WHERE average200 is not null order by date asc" % symbol
    cursor.execute(sql)
    return cursor.fetchall()


def getSpecDataForPlot(cursor, symbol, begDate, endDate):
    sql = "SELECT * FROM %s WHERE average200 is not null and date >= \"%s\" and date <= \"%s\" order by date asc" % (
        symbol, begDate, endDate)
    cursor.execute(sql)
    return cursor.fetchall()


def latestCloseAboveAverage200(cursor, symbol):
    latestDate = getLatestDate(cursor, symbol)
    sql1 = "SELECT close FROM %s WHERE date = \"%s\"" % (symbol, latestDate)
    cursor.execute(sql1)
    latestClose = float(cursor.fetchall()[0][0])
    sql2 = "SELECT average200 FROM %s WHERE date = \"%s\"" % (
        symbol, latestDate)
    cursor.execute(sql2)
    latestAverage200 = float(cursor.fetchall()[0][0])
    return latestClose >= latestAverage200


def dropTable(cursor, symbol):
    sql = "DROP TABLE %s" % symbol
    cursor.execute(sql)
