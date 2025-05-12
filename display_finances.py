import pandas as pd

OUT_FILE = "expenses.csv"

if __name__ == "__main__":
    df = pd.read_csv(OUT_FILE)
    for key, row in zip(df.columns.to_list()[1:], df.iloc[1][1:]):
        expenses_dict = eval(row)
        print(f"{key}: ", expenses_dict.get("acquisitions"), "\n\n")
