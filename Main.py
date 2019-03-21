import sqlite3
import pandas
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import datetime
from datetime import datetime
import array
import iso8601

def on_pick(event):
    type = event.artist()
    print(type)


# create database connetions
connection = sqlite3.connect("/home/Phil/store/Stock")
connection2 = sqlite3.connect("/home/Phil/store/News2")

# Should use read table but there is a bug
StockData = pandas.read_sql_query("SELECT * FROM dji", index_col="date", con=connection)
StockData["Unixdate"] = 0

NewsArticles = pandas.read_sql_query("SELECT * FROM data", index_col="date", con=connection2)
NewsArticles["Unixdate"] = 0

for entry in StockData.iterrows():
    date = datetime.fromisoformat(entry[0])
    stamp = datetime.timestamp(date)
    StockData.loc[entry[0], "Unixdate"] = stamp

for entry in NewsArticles.iterrows():
    NewsArticles.loc[entry[0], "Unixdate"] = iso8601.parse_date(entry[0])

x = 0

if x is 0:
    plt.subplot(211)
    plt.xticks(StockData["Unixdate"])
    plt.plot(StockData["1. open"], picker=5)
    plt.plot(StockData["2. high"], picker=5)
    plt.plot(StockData["3. low"], picker=5)
    plt.xticks(rotation=45)

    plt.subplot(212)
    plt.xticks(StockData["Unixdate"])
    #fig = plt.subplot(212)
    plt.plot(NewsArticles["Sentiment"], 'ro', picker=5)
    plt.xticks(rotation=45)

    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)

    #cid = fig.canvas.mpl_connect('button_press_event', on_pick)
    
if x is 1:
    mpl_fig = plt.figure()
    ax = mpl_fig.add_subplot(111)

    StockData.sort_values(by=["Unixdate"])

    ax.plot(StockData["Unixdate"],StockData["1. open"], lw=2)
    ax.plot(StockData["Unixdate"],StockData["2. high"], lw=2)
    ax.plot(StockData["Unixdate"],StockData["3. low"], lw=2)
    
else:
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Price')
    ax1.set_xlabel('Date')
    plt.yticks(StockData["Unixdate"])
    ax1.plot(StockData["1. open"])
    ax1.plot(StockData["2. high"])
    ax1.plot(StockData["3. low"])

    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Sentiment')  # we already handled the x-label with ax1

    ax2.plot(NewsArticles["Sentiment"], 'ro',  picker=5)
    ax2.tick_params(axis='y')

    cid = fig.canvas.mpl_connect('button_press_event', on_pick)

    fig.tight_layout()

plt.show()

connection.close()
connection2.close()
