from typing import Union, Any

import yaml
from pathlib import Path
import pandas as pd
from datetime import datetime

DATA = yaml.safe_load(Path("data.yaml").read_bytes())
OUT_FILE = "expenses.csv"


def get_acquisitions() -> dict[str, int]:
    return {
        "Amazon": 75,
        "Müllmarke": 93,
        "Air Force": 71,
        "Tanken": 80,
        "MacBook": 875,
    }


def get_cashouts() -> dict[str, int]:
    return {
        "interest": 4,
        "Weihnachten Kostyk": 50,
    }


def compute_expenses(
    fix_costs: dict[str, int],
    investments: dict[str, int],
    acquisitions: dict[str, int],
    cashouts: dict[str, int],
) -> Union[int, float]:
    total_expenses = 0

    for v in fix_costs.values():
        total_expenses += v

    if investments:
        for i in investments.values():
            total_expenses += i

    if acquisitions:
        for a in acquisitions.values():
            total_expenses += a

    if cashouts:
        for c in cashouts.values():
            total_expenses -= c

    return total_expenses


def create_current_month_dict() -> dict[str, Any]:
    data = DATA

    income = data["income"]
    fix_costs = data["fix_costs"]
    investments = data["investments"]

    acquisitions = get_acquisitions()
    cashouts = get_cashouts()

    total_expenses = compute_expenses(
        fix_costs=fix_costs,
        investments=investments,
        acquisitions=acquisitions,
        cashouts=cashouts,
    )

    return {
        "income": income,
        "expenses": {
            "fix_costs": fix_costs,
            "investments": investments,
            "acquisitions": acquisitions,
            "cashouts": cashouts,
        },
        "total_expenses": total_expenses,
        "cashouts": cashouts,
        "savings": income - total_expenses,
    }


def adjust_df(main_df: pd.DataFrame, update: dict) -> pd.DataFrame:
    current_month = f"{datetime.now().strftime('%B')}"

    main_df[current_month] = main_df["January"]
    main_df.index = ["income", "expenses", "total_expenses", "cashouts", "savings"]

    main_df[current_month][0] = update["income"]
    main_df[current_month][1] = update["expenses"]
    main_df[current_month][2] = update["total_expenses"]
    main_df[current_month][3] = update["cashouts"]
    main_df[current_month][4] = update["savings"]

    return clean_df(main_df)


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    column_names = df.columns
    for col in column_names:
        if col.__contains__("Unnamed"):
            df.drop(col, axis=1, inplace=True)

    return df


if __name__ == "__main__":
    monthly_update = create_current_month_dict()

    main_df = pd.read_csv(OUT_FILE)
    main_df = adjust_df(main_df=main_df, update=monthly_update)
    main_df.to_csv(OUT_FILE)

    loaded_df = pd.read_csv(OUT_FILE)

    print(loaded_df)
