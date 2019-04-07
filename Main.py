import sqlite3
import pandas
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import datetime
from datetime import datetime
import array
import pymysql

def on_pick(event):
    line = event.artist
    xdata, ydata = line.get_data()
    ind = event.ind
    data = NewsArticles.loc(ind[0])
    print(data)


# create database connetions
connection = sqlite3.connect("/home/Phil/store/Stock")
connection2 = sqlite3.connect("/home/Phil/store/News2")
gcloudcon = pymysql.connect(host='127.0.0.1',
                            database='store',
                            user='pmj5',
                            password='m4rjrmhg')
cur = gcloudcon.cursor()

# Should use read table but there is a bug
StockData = pandas.read_sql_query("SELECT * FROM dji ORDER BY date ASC", index_col="date", con=gcloudcon)
StockData["Unixdate"] = datetime(1970, 1, 1)

NewsArticles = pandas.read_sql_query("SELECT * FROM articles", index_col="date", con=gcloudcon)
NewsArticles["Unixdate"] = datetime(1970, 1, 1)
NewsArticles["NumsSentiment"] = 0.00001


for entry in StockData.iterrows():
    date = datetime.fromisoformat(entry[0])
    #stamp = datetime.timestamp(date)
    StockData.loc[entry[0], "Unixdate"] = date

for entry in NewsArticles.iterrows():
    x = 0
    Sent = ""
    for item in entry[1].iteritems():
        x += 1
        if x is 4:
            Sent = item[1]
    date = datetime.fromisoformat(entry[0])

    #stamp = datetime.timestamp(date)
    NewsArticles.loc[entry[0], "Unixdate"] = date
    try:
        num = float(Sent)
        NewsArticles.loc[entry[0], "NumsSentiment"] = num
    except:
        print("the fuck")



x = 9

if x is 0:

    NewsArticles.sort_values(by=["Unixdate"])
    StockData.sort_values(by=["Unixdate"])

    plt.subplot(211)
    #plt.xticks(StockData["Unixdate"])
    plt.plot(StockData["Unixdate"], StockData["open"], picker=5)
    plt.plot(StockData["Unixdate"], StockData["high"], picker=5)
    plt.plot(StockData["Unixdate"], StockData["low"], picker=5)
    plt.xticks(rotation=45)

    plt.subplot(212)
    #plt.xticks(StockData["Unixdate"])
    #fig = plt.subplot(212)
    plt.plot(NewsArticles["Unixdate"], NewsArticles["NumsSentiment"], 'ro', picker=5)
    plt.xticks(rotation=45)

    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)

    #cid = fig.canvas.mpl_connect('button_press_event', on_pick)
    
elif x is 1:
    mpl_fig = plt.figure()
    ax = mpl_fig.add_subplot(111)

    StockData.sort_values(by=["Unixdate"])

    ax.plot(StockData["Unixdate"],StockData["open"], lw=2)
    ax.plot(StockData["Unixdate"],StockData["high"], lw=2)
    ax.plot(StockData["Unixdate"],StockData["low"], lw=2)
    
    #cid = mpl_fig.canvas.mpl_connect('button_press_event', on_pick)
    
else:
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Price')
    ax1.set_xlabel('Date')
    
    NewsArticles.sort_values(by=["Unixdate"])
    StockData.sort_values(by=["Unixdate"])

    plt.yticks(StockData["Unixdate"])
    ax1.plot(StockData["Unixdate"], StockData["open"])
    ax1.plot(StockData["Unixdate"], StockData["high"])
    ax1.plot(StockData["Unixdate"], StockData["low"])

    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Sentiment')  # we already handled the x-label with ax1

    ax2.plot(NewsArticles["Unixdate"], NewsArticles["NumsSentiment"], 'ro',  picker=5)
    ax2.tick_params(axis='y')

    cid = fig.canvas.mpl_connect('pick_event', on_pick)

    #fig.tight_layout()

plt.show()

connection.close()
connection2.close()
