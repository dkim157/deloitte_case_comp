import pandas as pd

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

def create_stock_df(csv_file):
    stock = pd.read_csv(csv_file).drop(['High', 'Low', 'Adj Close', 'Volume'], 1)
    avg_df = get_avg(stock)
    stock.insert(3, "Avg", avg_df)

    return stock

def get_avg(stock):
    avg_df = []

    for index, row in stock.iterrows():
        avg_df.append((row["Open"] + row["Close"]) / 2)

    return avg_df

def combine_by_date(stock, div):

    for index, row in stock.iterrows():
       print(index, row["Date"])

if __name__ == "__main__":

    # create base tables
    stock = create_stock_df("./att_stock.csv")
    div = pd.read_csv("./att_div.csv")

    # sort and reformat dates
    stock = stock.sort_values("Date")
    div = div.sort_values("Date")
    stock["Date"] = stock["Date"].apply(lambda x: format_date(x))
    div["Date"] = div["Date"].apply(lambda x: format_date(x))

    # figure out how to actually combine the two
    frames = [stock, div]
    result = combine_by_date(stock, div)
    #result = pd.concat(frames)

    #print(result)