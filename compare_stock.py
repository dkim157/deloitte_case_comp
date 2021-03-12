import pandas as pd
import numpy as np

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

    # combine stock and div
    result = combine_by_date(stock, div)

    # add Div Yield
    result["Div Yield"] = np.nan
    add_div_yield(result)

    return result

def add_div_yield(result):
    sum_avg = 0
    ctr = 0

    for i in range(len(result)):
        avg = result.loc[i, "Avg"]
        div = result.loc[i, "Div"]

        if not np.isnan(avg):  # add to avg
            sum_avg += avg
        if not np.isnan(div):  # calc and add Div Yield
            if ctr-1 > 0:
                result.loc[i, "Div Yield"] = div/(sum_avg/(ctr-1))
            sum_avg = 0
            ctr = 0
        ctr += 1

def add_years(stock, stock_name, output, cols):
    year = 0

    for i in range(len(stock)):
        prev_year = year
        year = stock.loc[i, "Date"][:4]
        if year != prev_year:
            yr = pd.DataFrame([[stock_name + " (" + year + ")", np.nan, np.nan, np.nan, np.nan]], columns=cols)
            output = output.append(yr, ignore_index=True)

    return output

# return index after first div -- will be slightly off
def get_start_idx(stock):

    for i in range(len(stock)):
        new_div = stock.loc[i, "Div"]

        if not np.isnan(new_div):
            return i+1


def add_avg_price(stock, output):
    avg = 0
    index = 5

    month_ctr = 0
    for i in range(len(stock)-1, -1, -1):
        tmp = stock.loc[i, "Avg"]
        if not np.isnan(tmp):
            avg += tmp
            month_ctr += 1
        if (month_ctr == 12) or (i == 0):
            avg = avg/12
            if(avg != 0):
                output.loc[index, "Avg Price"] = avg
            index -= 1
            month_ctr = 0
            avg = 0



def add_change_in_price(output):
    prev_price = output.loc[0, "Avg Price"]

    for i in range(1, len(output)):
        new_price = output.loc[i, "Avg Price"]
        output.loc[i, "Change in Price"] = (new_price-prev_price)/prev_price
        prev_price = new_price

def add_annual_div_yield(output, stock):

    # create list of stock divs
    div_lst = []
    for i in range(len(stock)-1, -1, -1):
        tmp = stock.loc[i, "Div"]
        if not np.isnan(tmp):
            div_lst.append(tmp)
    div_lst = pd.unique(div_lst).tolist()

    for i in range(len(output)-1, 0, -1):
        output.loc[i, "Div Yield"] = (div_lst.pop(0)*4)/output.loc[i, "Avg Price"]

def add_div_growth_rate(output):
    prev_price = output.loc[0, "Div Yield"]

    for i in range(1, len(output)):
        new_price = output.loc[i, "Div Yield"]
        output.loc[i, "Div Growth Rate"] = (new_price - prev_price) / prev_price
        prev_price = new_price

def create_out_df(stock, stock_name):
    cols = ['Year', 'Avg Price', 'Change in Price', 'Div Yield', 'Div Growth Rate']

    output = pd.DataFrame(columns=cols)
    output = add_years(stock, stock_name, output, cols)
    add_avg_price(stock, output)
    add_change_in_price(output)
    add_annual_div_yield(output, stock)
    add_div_growth_rate(output)

    output = output.drop(output.index[0]).reset_index(drop=True)

    return output

def print_values(name):
    stock = create_stock_df(name)
    out = create_out_df(stock, name)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(stock)
        print(out)

if __name__ == "__main__":

    stock_names = ["APPL", "IBM", "KO", "NHI", "T"]

    for name in stock_names:
        # create dataframes
        stock = create_stock_df(name)
        out = create_out_df(stock, name)
        # create .csv files
        stock.to_csv(r'./output/' + name + '_full.csv', index=False)
        out.to_csv(r'./output/' + name + '_summary.csv', index=False)

    # print_values("APPL")