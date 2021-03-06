import requests
import json
from multiDB import TableManager
import time


def buildUrl(symbol):
  # Zu Base-Url wird API-Key und Kürzel hinzugefügt
    url = "https://www.alphavantage.co/query"
    url += "?function=TIME_SERIES_DAILY_ADJUSTED"
    url += "&outputsize=full"
    url += "&apikey="
    url += open("apikey.txt").read()
    url += "&symbol="
    url += symbol
    return url


starting_conf = json.loads(open("config.json").read())

for symbol in starting_conf["stocks"]:
    tb = TableManager(symbol)
    tb.createTable()
    url = buildUrl(tb.getSymbol())
    print("%s: %s" % (tb.getSymbol().upper(), url))

    response = requests.get(url).content
    jsonData = json.loads(response)

    if "Time Series (Daily)" in jsonData:
        jsonData = jsonData["Time Series (Daily)"]

    elif "Note" in jsonData:
        print("Bandwidth exhausted (max. 5 requests per minute)")
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

            close = round(float(jsonData[date]["5. adjusted close"]), 2)
            tb.insertClose(date, close)
            counter += 1

        if counter == 0:
            print("  DB is up-to-date.")
        else:
            print("  " + str(counter) + " days updated.")

    else:
        print("  Table \"%s\" is empty. Saving full API call.\n" %
              tb.getSymbol())

        split_coefficient = 1.0

        for date in jsonData:

            current_split = jsonData[date]["8. split coefficient"]

            close = float(jsonData[date]["4. close"])
            close /= split_coefficient
            close = round(close, 2)
            
            if jsonData[date]["8. split coefficient"] != "1.0":
                print("  Split on %s with value %s" %
                      (date, jsonData[date]["8. split coefficient"]))
                tb.deleteSplits()
                tb.insertSplit(date, jsonData[date]["8. split coefficient"])
            
            # close = round(float(jsonData[date]["5. adjusted close"]), 4)
            tb.insertClose(date, close)
            
            split_coefficient *= float(current_split)

    tb.commit()

    dbData = tb.getAllData()
    moving_average_days = 200

    for i in range(tb.getTableSize() - moving_average_days):
        sum = 0

        for j in range(moving_average_days):
            sum += dbData[i+j][1]

        result = sum / moving_average_days
        result = round(result, 4)
        tb.insertAverage200(dbData[i][0], result)

    tb.commit()
    print("  Moving average calculated and saved to DB.\n\n")

    if len(starting_conf["stocks"]) >= 4:
        time.sleep(15)
