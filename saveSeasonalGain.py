from multiDB import TableManager
from datetime import date

stocks = open("stocks.txt").read().split(",")
tb = TableManager("TSLA")
tb.deleteFromSaisonal()

for stock in stocks:
    tb = TableManager(stock)
    latestDate = date.fromisoformat(tb.getLatestDate())
    year = latestDate.year
    month = latestDate.month - 1

    while year != latestDate.year - 10 or month != latestDate.month:
        monthData = tb.getDataForRanking(str(month), str(year))
        diff = monthData[-1][1] - monthData[0][1]
        gain = diff / monthData[0][1]
        tb.insertSaisonal(tb.getSymbol(), year, month, gain)

        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1

    tb.commit()
