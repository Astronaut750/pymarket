import requests
import json
import db


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
    jsonData = json.loads(response)["Time Series (Daily)"]


# Verbinden mit DB und Tabelle erstellen
conn = db.open()
cursor = conn.cursor()
db.createTable(cursor, symbol)


# Überprüfung ob schon genügend Daten vorhanden sind
if db.getTableSize(cursor, symbol) > 1000:
  print("Zum angegebenen Ticker exisitert bereits eine Tabelle mit über 1000 Einträgen.\n")

  # Aktualität überprüfen
  latestDbEntry = db.getMostRecentDate(cursor,symbol)
  print("Letzer Eintrag in der Datenbank: " + latestDbEntry)

  latestApiEntry = next(iter(jsonData))
  print("Letzer Eintrag in der API:       " + latestApiEntry + "\n")

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

else:
  print("Zum angegebenen Ticker gibt es noch nicht ausreichend Daten.")
  print("Alle abgefragten Daten werden in die Datenbank übernommen.")

  for day in jsonData:
    close = jsonData[day]["4. close"]
    values = (day, close, close)
    db.insertClose(cursor, symbol, values)

# Am Ende müssen alle geänderten Einträge übernommen werden
conn.commit()


