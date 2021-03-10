# pymarket

A python script that fetches data from the Alphavantage Stockmarket API, saves it to a MySQL database, calculates the moving average over 200 days per day and plots a graph with both lines.

Librarys:
* "mysql-connector-python" to connect to the database
* "matplotlib" to plot the graph

Features:
* Split correction
* Reading stocks from file "stocks.txt"
* Fetching multiple stocks at once
* Plotting multiple graphs consecutively.

When a split is detected while updating a stock, updating is cancelled. The table gets deleted and, after the other stocks are finished calculating, it is queried again from the api.

If the latest close value of a stock is higher than the moving average, the background of the plot is green, otherwise it's red.

Usage:
1. Get an API-Key from www.alphavantage.co and save it to a file called "apikey.txt"
2. Write your desired stocks into the "stocks.txt" file in CSV style
3. Run "multiMain.py"
4. Run "multiPlot.py"

![sampleMultiMainOutput](https://user-images.githubusercontent.com/38164738/110682689-812d9080-81db-11eb-80e7-c5c5f02e1a92.JPG)

![sampleTslaPlot](https://user-images.githubusercontent.com/38164738/110682700-84c11780-81db-11eb-9a48-cc89694f5b70.JPG)

![sampleAmdPlot](https://user-images.githubusercontent.com/38164738/110682706-868adb00-81db-11eb-872f-90437d3c5940.JPG)
