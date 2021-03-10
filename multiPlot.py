from multiDB import TableManager
from matplotlib import pyplot as plt
from datetime import date as dt


def fiso(date):
    return dt.fromisoformat(date)


# Not all stocks have the same first date, so for apple 2009-01-01 would be a valid date
# but not for tsla which only have stock data starting in 2010
# This function returns the "latest" or "most recent" first date from all stocks


def latestFirstDate(stocks):
    firstdate = fiso("1900-01-01")
    for symbol in stocks:
        tb = TableManager(symbol)
        if fiso(tb.getFirstDate()) > firstdate:
            firstdate = fiso(tb.getFirstDate())
    return firstdate


def inputDate(nr, begDate=""):
    lfd = latestFirstDate(stocks)
    latestDate = fiso(tb.getLatestDate())

    print("Input only from %s to %s and in ISO format (YYYY-MM-DD)." %
          ((lfd, latestDate) if nr == 1 else (begDate, latestDate)))

    while True:
        date = input("Beginning date ('x' for %s): " % lfd if nr == 1 else
                     "Ending date ('x' for %s): " % latestDate)
        if date.lower() == "x":
            return str(lfd) if nr == 1 else str(latestDate)
        try:
            date = fiso(date)
            if date < (lfd if nr == 1 else fiso(begDate)) or date > latestDate:
                print("Date out of range.\n")
            else:
                return str(date)
        except:
            print("Wrong date format.\n")


def plot(dbData):
    dates = []
    close = []
    average200 = []
    for date in dbData:
        dates.append(fiso(date[0]))
        close.append(date[1])
        average200.append(date[2])

    fig, ax = plt.subplots()
    ax.plot(dates, close)
    ax.plot(dates, average200)
    plt.xlabel("dates")
    plt.ylabel("close & average200")
    plt.title(tb.getSymbol())
    if tb.isLatestCloseAboveAverage200():
        ax.set_facecolor("xkcd:light green")
    else:
        ax.set_facecolor("xkcd:peach")
    plt.show()


stocks = open("stocks.txt").read().split(",")

global tb
begDate = None
endDate = None

for symbol in stocks:
    tb = TableManager(symbol)

    if not begDate:
        begDate = inputDate(1)
        endDate = inputDate(2, begDate)

    plot(tb.getSpecDataForPlot(begDate, endDate))
