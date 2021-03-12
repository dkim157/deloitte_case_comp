import pandas as pd

def get_avg(stock):
    avg_df = []

    for index, row in stock.iterrows():
        avg_df.append((row["Open"] + row["Close"]) / 2)

    return avg_df

def open_stock_df(csv_file):
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

def create_stock_df(stock_name):
    # create base tables
    stock = open_stock_df("./" + stock_name + "_stock.csv")
    div = pd.read_csv("./" + stock_name + "_div.csv")

    # sort (and reformat) dates
    stock = stock.sort_values("Date")
    div = div.sort_values("Date")

    result = combine_by_date(stock, div)
    return result

if __name__ == "__main__":

    result = create_stock_df("APPL")

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(result)
