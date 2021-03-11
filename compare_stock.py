import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("./at&t.csv").drop(['Adj Close', 'Volume'], 1)
    print(df)