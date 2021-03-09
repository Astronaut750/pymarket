import requests
import json
from multiDB import TableManager


def buildUrl(symbol):
  # Zu Base-Url wird API-Key und Kürzel hinzugefügt
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&apikey="
    url += open("apikey.txt").read()
    url += "&symbol=" + symbol
    return url


stocks = open("stocks.txt").read().split(",")

for symbol in stocks:
    print("%s:" % symbol.upper())
    tb = TableManager(symbol)
    tb.createTable()
    url = buildUrl(tb.getSymbol())
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

    if tb.getTableSize() > 1000:
        print("  Symbol \"%s\" already has 1000+ entries in DB\n" %
              tb.getSymbol())

        latestDbEntry = tb.getLatestDate()
        print("  Latest DB Entry:  %s" % latestDbEntry)
        latestApiEntry = next(iter(jsonData))
        print("  Latest API Entry: %s\n" % latestApiEntry)

        counter = 0
        splitfound = False
        for date in jsonData:
            if date == latestDbEntry:
                break

            if date == "2021-03-01":
                jsonData[date]["8. split coefficient"] = "5.0"

            if jsonData[date]["8. split coefficient"] != "1.0":
                print("! Found split at %s while trying to update table.\n\n" % date)
                stocks.append(tb.getSymbol())
                tb.dropTable()
                splitfound = True
                break

            close = jsonData[date]["4. close"]
            tb.insertClose(date, close)
            counter += 1

        if splitfound:
            continue

        if counter == 0:
            print("  DB is up-to-date.")
        else:
            print("  " + str(counter) + " days updated.")

    else:
        print("  Symbol \"%s\" does not have enough data in DB. Saving full API call.\n" %
              tb.getSymbol())

        split_coefficient = 1.0

        for date in jsonData:
            current_split = jsonData[date]["8. split coefficient"]

            close = float(jsonData[date]["4. close"])
            close /= split_coefficient
            close = round(close, 2)
            tb.insertClose(date, close)
            split_coefficient *= float(current_split)

            if current_split != "1.0":
                print("  Split on %s with value %s." % (date, current_split))
                print("  Split now at %s.\n" % split_coefficient)

    tb.commit()

    dbData = tb.getAllData()
    moving_average_days = 200

    for i in range(tb.getTableSize() - moving_average_days):
        sum = 0
        for j in range(moving_average_days):
            sum += dbData[i + j][1]

        result = sum / moving_average_days
        result = round(result, 2)
        tb.insertAverage200(dbData[i][0], result)

    tb.commit()
    print("  Moving average calculated and saved to DB.\n\n")
