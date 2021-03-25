from multiDB import TableManager


def calculateAverageGain(symbol, years, month):
    tb = TableManager(symbol)
    gains = tb.getGainsForMonth(month)
    avg = 0.0

    for i in range(years):
        try:
            avg += gains[i][3]
        except:
            print("Only %s years available." % str(i + 1))
            years = i + 1
            break

    return (years, round(avg / years, 5))


symbol = input("Stock ticker: ")
years = int(input("How many years: "))
month = int(input("Which month: "))
result = calculateAverageGain(symbol, years, month)
print("\nAvgGain (%s years): %s" % result)
