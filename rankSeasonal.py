from multiDB import TableManager
from datetime import date
import json
import calendar

config = json.loads(open("rankingConfig.json").read())
stocks = open("stocks.txt").read().split(",")

for month in range(12):
    monthname = calendar.month_name[month + 1]
    rankings = []

    for stock in stocks:
        tb = TableManager(stock)
        date = date.fromisoformat(tb.getLatestDate())

        if date.month > month:
            year = date.year
        else:
            year = date.year - 1

        avg = 0.0

        for i in range(config["years"]):
            monthData = tb.getDataForRanking(str(month+1), str(year))
            difference = monthData[-1][1] - monthData[0][1]
            rise = difference / monthData[0][1]
            avg += rise
            year -= 1

        avg = round(avg / config["years"] * 100, 3)
        rankings.append((avg, stock))

    rankings.sort(reverse=True)

    print("\nTop 5 in " + monthname + ":")
    for i in range(5):
        print("%5s  %5s %%" % (rankings[i][1].upper(), rankings[i][0]))
