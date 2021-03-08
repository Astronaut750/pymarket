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
    sql = "CREATE TABLE IF NOT EXISTS " + symbol + \
        " (date char(10) PRIMARY KEY, close real, average200 real)"
    cursor.execute(sql)

def insertClose(cursor, symbol, values):
    sql = "INSERT INTO " + symbol + \
        " (date, close) VALUES(%s, %s) ON DUPLICATE KEY UPDATE close = %s"
    cursor.execute(sql, values)

def insertAverage200(cursor, symbol, values):
    sql = "UPDATE " + symbol + " SET average200 = "+ values[0] +" WHERE date = \""+ values[1] +"\";"
    cursor.execute(sql)

def getTableSize(cursor, symbol):
    sql = "SELECT date FROM " + symbol
    cursor.execute(sql)
    result = cursor.fetchall()
    return len(result)

def getMostRecentDate(cursor, symbol):
    sql = "SELECT date FROM " + symbol + " ORDER BY date DESC"
    cursor.execute(sql)
    return cursor.fetchall()[0][0]

def getAllData(cursor, symbol):
    sql = "SELECT * FROM " + symbol + " ORDER BY date DESC"
    cursor.execute(sql)
    return cursor.fetchall()

def dropTable(cursor, symbol):
    sql = "DROP TABLE " + symbol
    cursor.execute(sql)
