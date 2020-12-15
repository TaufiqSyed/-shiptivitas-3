import sqlite3
import datetime
import julian

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

conn = sqlite3.connect('shiptivity.db')
c = conn.cursor()

def get_feature_change_date():
    c.execute('''
        SELECT MIN(round(julianday(datetime(timestamp, 'unixepoch', 'localtime')) - 0.5))
        AS feature_change_day_number
        FROM card_change_history;
    ''')
    data = c.fetchall()[0][0]
    return julian.from_jd(data, fmt='jd')

def graph_daily_user_count():
    c.execute('SELECT day_number, user_count FROM daily_user_count')
    data = c.fetchall()

    dates = []
    values = []
    for row in data:
        dates.append(julian.from_jd(row[0], fmt='jd'))
        values.append(row[1])
    
    fig, ax = plt.subplots()

    ax.plot(dates, values)
    plt.axvline(
        x=get_feature_change_date(), 
        label='Feature Change', 
        color='r', 
        linestyle='--'
    )

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.set_xlim(dates[0], dates[-1])
    plt.ylim(0, max(values))
    fig.autofmt_xdate()
    plt.xlabel('Year')
    plt.ylabel('Daily User Count')
    plt.legend()

    plt.show()

def graph_status_changes_by_card():
    c.execute('SELECT cardId, status_change_count FROM card_status_change_count')
    data = c.fetchall()
    card_id, status_change_count = [[ i for i, j in data], [ j for i, j in data]] 

    ax = plt.subplots()[1]

    ax.bar(card_id, status_change_count)
    plt.xlabel('Card ID')
    plt.ylabel('Number of Status Changes')
    ax.set_xticks(list(range(1, max(card_id))), minor=True)

    plt.show()

graph_daily_user_count()
graph_status_changes_by_card()
c.close
conn.close()

