import requests
import json
from multiDB import TableManager
import time

def buildUrl(symbol):
  # Zu Base-Url wird API-Key und Kürzel hinzugefügt
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&apikey="
    url += open("apikey.txt").read()
    url += "&symbol=" + symbol
    return url


stocks = open("stocks.txt").read().split(",")

for symbol in stocks:
    tb = TableManager(symbol)
    tb.createTable()
    url = buildUrl(tb.getSymbol())
    print("%s: %s" % (tb.getSymbol().upper(), url))

    response = requests.get(url).content
    jsonData = json.loads(response)

    if "Time Series (Daily)" in jsonData:
        jsonData = jsonData["Time Series (Daily)"]

    elif "Note" in jsonData:
        print("Bandwidth exhausted (max. 5 per minute)")
        break

    elif "Error Message" in jsonData:
        print("Symbol \"%s\" not found" % tb.getSymbol())
        continue

    else:
        print("Error while trying keys on API data")
        print(jsonData)
        break

    if tb.getTableSize() > 0:
        print("  Table \"%s\" is not empty. Updating DB.\n" %
              tb.getSymbol())

        latestDbEntry = tb.getLatestDate()
        print("  Latest DB Entry:  %s" % latestDbEntry)
        latestApiEntry = next(iter(jsonData))
        print("  Latest API Entry: %s\n" % latestApiEntry)

        counter = 0
        for date in jsonData:
            if date == latestDbEntry:
                break

            close = jsonData[date]["5. adjusted close"]
            tb.insertClose(date, close)
            counter += 1

        if counter == 0:
            print("  DB is up-to-date.")
        else:
            print("  " + str(counter) + " days updated.")

    else:
        print("  Table \"%s\" is empty. Saving full API call.\n" %
              tb.getSymbol())

        for date in jsonData:
            close = jsonData[date]["5. adjusted close"]
            tb.insertClose(date, close)

    tb.commit()

    dbData = tb.getAllData()
    moving_average_days = 200

    for i in range(tb.getTableSize() - moving_average_days):
        sum = 0

        for j in range(moving_average_days):
            sum += dbData[i+j][1]

        result = sum / moving_average_days
        result = round(result, 2)
        tb.insertAverage200(dbData[i][0], result)

    tb.commit()
    print("  Moving average calculated and saved to DB.\n\n")
    time.sleep(15)
