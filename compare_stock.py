import pandas as pd

if __name__ == "__main__":
    data = {'Name': ['Tom', 'Jack', 'Steve', 'Ricky'], 'Age': [28, 34, 29, 42]}
    df = pd.DataFrame(data)
    print(df)