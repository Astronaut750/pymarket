import singleDB
from matplotlib import pyplot as plt
from datetime import date as dt


def inputDate(nr, cursor, symbol, begDate="1901-01-01"):
    inputInvalid = True
    while inputInvalid:
        date = input("Datum %s (YYYY-MM-DD): " % nr)
        try:
            date = dt.fromisoformat(date)
            if date < dt.fromisoformat(singleDB.getFirstDate(cursor, symbol)) or date > dt.fromisoformat(singleDB.getLatestDate(cursor, symbol)):
                print("Date out of Range\n")
                continue
            elif date < dt.fromisoformat(begDate):
                print("Date 2 before Date 1\n")
                continue
            return str(date)
        except ValueError:
            print("Falsches Format!\n")


def plot(cursor, symbol, dbData):
    dates = []
    close = []
    average200 = []
    for date in dbData:
        # Creating a list for the plot
        dates.append(dt.fromisoformat(date[0]))
        close.append(date[1])
        average200.append(date[2])

    fig, ax = plt.subplots()
    ax.plot(dates, close)
    ax.plot(dates, average200)
    plt.xlabel("dates")
    plt.ylabel("close & average200")
    plt.title(symbol)
    if singleDB.latestCloseAboveAverage200(cursor, symbol):
        ax.set_facecolor("xkcd:peach")
    else:
        ax.set_facecolor("xkcd:light green")
    plt.show()


conn = singleDB.open()
cursor = conn.cursor()
symbol = "tsla"

#begDate = inputDate(1, cursor, symbol)
#endDate = inputDate(2, cursor, symbol, begDate)

plot(cursor, symbol, singleDB.getAllDataForPlot(cursor, symbol))
#plot(cursor, symbol, singleDB.getSpecDataForPlot(cursor, symbol, begDate, endDate))
