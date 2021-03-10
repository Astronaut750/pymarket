# pymarket

A program, which fetches data from the Alphavantage API, saves it to a MySQL database, calculates the moving average over 200 days per day and plots a graph with both lines.

Used librarys:
"mysql-connector-python" to connect to the database
"matplotlib" to plot the graph

Implemented split correction, reading stocks from file "stocks.txt" to call api with multiple stocks, plotting multiple graphs consecutively.
When a split is detected while updating a stock, updating is cancelled, the table gets deleted and, after the other stocks are finished calculating, it is queried again from the api.

If the latest close value of a stock is higher than the moving average, the background of the plot is green, otherwise it's red.

Usage:

1. Write your desired stocks into the "stocks.txt" file in CSV style.
2. Run "multiMain.py"
3. Run "multiPlot.py"
