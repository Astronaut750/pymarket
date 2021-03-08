from re import split
import requests
import json
import db

# Standard input für Extension AREPL
standard_input = "tsla"

def buildUrl(symbol):
  # Zu Base-Url wird API-Key und Kürzel hinzugefügt
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&apikey="
    url += open("apikey.txt").read()
    url += "&symbol=" + symbol
    return url




# Eingabe des Symbols, Überprüfung und Auslesen der API
jsonData = None
symbolInvalid = True

while symbolInvalid:
  symbol = input("Aktien-Ticker: ")

  url = buildUrl(symbol)
  response = requests.get(url).content

  try:
    json.loads(response)["Error Message"]
    symbolInvalid = True
    print("Der Ticker wurde nicht gefunden. Bitte versuchen Sie eine andere Aktie.\n")
  except:
    symbolInvalid = False
    jsonData = json.loads(response)
    jsonData = jsonData["Time Series (Daily)"]


# Verbinden mit DB und Tabelle erstellen
conn = db.open()
cursor = conn.cursor()
db.createTable(cursor, symbol)




# Überprüfung ob schon genügend Daten vorhanden sind
split_coefficient = 1.0
if db.getTableSize(cursor, symbol) > 1000:
  print("Zum angegebenen Ticker exisitert bereits eine Tabelle mit über 1000 Einträgen.\n")

  # Aktualität überprüfen
  latestDbEntry = db.getMostRecentDate(cursor,symbol)
  print("Letzer Eintrag in der Datenbank: %s" % latestDbEntry)

  latestApiEntry = next(iter(jsonData))
  print("Letzer Eintrag in der API:       %s\n" % latestApiEntry)
  
  # Daten bis letzten vorhandenen Tag eintragen
  counter = 0
  for day in jsonData:
    if day == latestDbEntry:
      break

    close = jsonData[day]["4. close"]
    values = (day, close, close)
    db.insertClose(cursor, symbol, values)
    counter += 1
  
  if counter == 0:
    print("Datenbank ist aktuell.")
  else:
    print(str(counter) + " Tage aktualisiert.")
  del counter

else:
  print("Zum angegebenen Ticker gibt es noch nicht ausreichend Daten.")
  print("Alle abgefragten Daten werden in die Datenbank übernommen.")

  for day in jsonData:
    current_split = jsonData[day]["8. split coefficient"]
    if current_split != "1.0":
      closeFloat = float(jsonData[day]["4. close"]) / split_coefficient
      closeFloat = round(closeFloat, 2)
      close = str(closeFloat)
      split_coefficient *= float(current_split)

      print("Split on %s with value %s." % (day, current_split))
      print("Split now at %s." % split_coefficient)
      continue

    closeFloat = float(jsonData[day]["4. close"]) / split_coefficient
    closeFloat = round(closeFloat, 2)
    close = str(closeFloat)

    values = (day, close, close)
    db.insertClose(cursor, symbol, values)

# Am Ende müssen alle geänderten Einträge übernommen werden
conn.commit()
del jsonData




dbData = db.getAllData(cursor, symbol)
moving_average_days = 200

for i in range(len(dbData) - moving_average_days):
  sum = 0
  for j in range(moving_average_days):
    sum += dbData[i + j][1]
  
  result = round(sum / moving_average_days, 2)
  values = (str(result), dbData[i][0])
  db.insertAverage200(cursor, symbol, values)

conn.commit()
print("Moving average für alle Tage berechnet und abgespeichert.")
del dbData




