import pandas as pd

OUT_FILE = "expenses.csv"

if __name__ == "__main__":
    print(pd.read_csv(OUT_FILE)["December"][4])
