import pandas as pd
import numpy as np

def format_date(date):
    date = date[5:7] + "/" + date[8:] + "/" + date[2:4]
    return date

# -1 if date1 < date2
# 0 if date1 == date2
# 1 if date1 > date2
def compare_date(date1, date2):
    yr1 = date1[6:]
    mo1 = date1[:2]
    day1 = date1[3:5]

    yr2 = date2[6:]
    mo2 = date1[:2]
    day2 = date1[3:5]

    if yr1 != yr2: return int(yr1) - int(yr2)
    if mo1 != mo2: return int(mo1) - int(mo2)
    if day1 == day2: return 0
    else: return day1 - day2

def get_avg(stock):
    avg_df = []

    for index, row in stock.iterrows():
        avg_df.append((row["Open"] + row["Close"]) / 2)

    return avg_df

def create_stock_df(csv_file):
    stock = pd.read_csv(csv_file).drop(['High', 'Low', 'Adj Close', 'Volume'], 1)
    avg_df = get_avg(stock)
    stock.insert(3, "Avg", avg_df)

    return stock

def combine_by_date(stock, div):
    # 1. add and sort div dates to stock dates
    div_dates = div[['Date']].copy()
    result = stock.append(div_dates).sort_values("Date")

    # 2. add and sort stock dates to div dates
    stock_dates = stock[['Date']].copy()
    div = div.append(stock_dates).sort_values("Date")
    div = div.rename(columns={"Dividends": "Div"}).reset_index(drop=True)

    # 3. merge
    result = pd.merge(result, div, on="Date", how="outer")

    return result

if __name__ == "__main__":

    # create base tables
    stock = create_stock_df("./T_stock.csv")
    div = pd.read_csv("./T_div.csv")

    # sort (and reformat) dates
    stock = stock.sort_values("Date")
    div = div.sort_values("Date")
    #stock["Date"] = stock["Date"].apply(lambda x: format_date(x))
    #div["Date"] = div["Date"].apply(lambda x: format_date(x))

    result = combine_by_date(stock, div)
    
    print(result)
