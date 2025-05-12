import json

CURRENT_AGE = 25
RENT_AGE = 67

MONTHS_IN_RENT = 23 * 12

STARTING_CAPITAL = 0
MONTHLY_RATES = [200, 300, 400]
TAX_RATE = 0.25

YEARLY_INTEREST_RATE = 0.06
YEARLY_INFLATION_RATE = 0.02
YEARLY_COMMISSION_RATE_PR = 0.0074
YEARLY_COMMISSION_RATE_BR = 0.0079
REINVESTMENT_FACTOR = 0.4

monthly_interest_rate = YEARLY_INTEREST_RATE / 12
monthly_inflation_rate = YEARLY_INFLATION_RATE / 12
monthly_commission_rate_pr = YEARLY_COMMISSION_RATE_PR / 12
monthly_commission_rate_br = YEARLY_COMMISSION_RATE_BR / 12

inflation_in_rent = (1 - YEARLY_INFLATION_RATE) ** (RENT_AGE - CURRENT_AGE)

data = {}
for rate in MONTHLY_RATES:
    capital_without_interest_for_br = STARTING_CAPITAL
    capital_without_interest = STARTING_CAPITAL
    capital_with_inflation = STARTING_CAPITAL
    capital_with_interest = STARTING_CAPITAL
    capital_with_interest_and_inflation = STARTING_CAPITAL
    capital_with_interest_and_commision = STARTING_CAPITAL
    capital_with_interest_and_inflation_and_commision = STARTING_CAPITAL
    capital_with_interest_and_commision_and_reinvestment = STARTING_CAPITAL

    for months in range((RENT_AGE - CURRENT_AGE) * 12):
        # Kapital
        capital_without_interest += rate
        capital_without_interest_for_br += rate

        # Kapital mit Inflation
        capital_with_inflation += rate
        capital_with_inflation *= 1 - monthly_inflation_rate
        capital_with_inflation = round(capital_with_inflation, 2)

        # Kapital mit Zinseszins
        capital_with_interest += rate
        capital_with_interest *= 1 + monthly_interest_rate
        capital_with_interest = round(capital_with_interest, 2)

        # Kapital mit Zinseszins und Inflation
        capital_with_interest_and_inflation += rate
        capital_with_interest_and_inflation *= 1 + (
            monthly_interest_rate - monthly_inflation_rate
        )
        capital_with_interest_and_inflation = round(
            capital_with_interest_and_inflation, 2
        )

        # Kapital mit Zinseszins und Kosten der PR
        capital_with_interest_and_commision += rate
        capital_with_interest_and_commision *= 1 + (
            monthly_interest_rate - monthly_commission_rate_pr
        )
        capital_with_interest_and_commision = round(
            capital_with_interest_and_commision, 2
        )

        # Kapital mit Zinseszins, Inflation und Kosten der PR
        capital_with_interest_and_inflation_and_commision += rate
        capital_with_interest_and_inflation_and_commision *= 1 + (
            monthly_interest_rate - monthly_inflation_rate - monthly_commission_rate_pr
        )
        capital_with_interest_and_inflation_and_commision = round(
            capital_with_interest_and_inflation_and_commision, 2
        )

        # Kapital mit Zinseszins und Reinvestition bei BR
        capital_with_interest_and_commision_and_reinvestment += rate
        capital_with_interest_and_commision_and_reinvestment *= 1 + (
            monthly_interest_rate - monthly_commission_rate_br
        )
        if months / 12 in list(range(45)):
            capital_with_interest_and_commision_and_reinvestment += (
                rate * 12 * REINVESTMENT_FACTOR
            )
            capital_without_interest_for_br += rate * 12 * REINVESTMENT_FACTOR
        capital_with_interest_and_commision_and_reinvestment = round(
            capital_with_interest_and_commision_and_reinvestment, 2
        )

    data[rate] = {
        "Ohne Inflation": {
            "Kapital ohne Zinsen": f"{capital_without_interest} €",
            "Kapital mit Zinsen": f"{capital_with_interest} €",
            "Kapital mit privater Rente": f"{capital_with_interest_and_commision} €",
            "Kapital mit Basisrente": f"{capital_with_interest_and_commision_and_reinvestment} €",
            "Differenz": f"{round(capital_with_interest - capital_with_interest_and_commision, 2)} €",
            "zu versteuern privat": f"{round(capital_with_interest - capital_without_interest, 2)} €",
            "nach Steuern privat": f"{round((capital_with_interest - capital_without_interest) * (1 - TAX_RATE), 2)} €",
            "Restsumme privat": f"{round((capital_with_interest - capital_without_interest) * (1 - TAX_RATE) + capital_without_interest, 2)} €",
            "monatliche Rente privat": f"{round(((capital_with_interest - capital_without_interest) * (1 - TAX_RATE) + capital_without_interest) / MONTHS_IN_RENT, 2)} €",
            "zu versteuern PR": f"{round(capital_with_interest_and_commision - capital_without_interest, 2)} €",
            "nach Steuern PR": f"{round((capital_with_interest_and_commision - capital_without_interest) * (1 - TAX_RATE / 2), 2)} €",
            "Restsumme PR": f"{round((capital_with_interest_and_commision - capital_without_interest) * (1 - TAX_RATE / 2) + capital_without_interest, 2)} €",
            "monatliche Rente PR": f"{round(((capital_with_interest_and_commision - capital_without_interest) * (1 - TAX_RATE / 2) + capital_without_interest) / MONTHS_IN_RENT, 2)} €",
            "zu versteuern BR": f"{round(capital_with_interest_and_commision_and_reinvestment - capital_without_interest_for_br, 2)} €",
            "nach Steuern BR": f"{round((capital_with_interest_and_commision_and_reinvestment - capital_without_interest_for_br) * (1 - TAX_RATE), 2)} €",
            "Restsumme BR": f"{round((capital_with_interest_and_commision_and_reinvestment - capital_without_interest_for_br) * (1 - TAX_RATE) + capital_without_interest, 2)} €",
            "monatliche Rente BR": f"{round(((capital_with_interest_and_commision_and_reinvestment - capital_without_interest_for_br) * (1 - TAX_RATE) + capital_without_interest) / MONTHS_IN_RENT, 2)} €",
        },
        "Mit Inflation": {
            "Kapital ohne Zinsen": f"{capital_with_inflation} €",
            "Kapital mit Zinsen": f"{capital_with_interest_and_inflation} €",
            "Kapital mit privater Rente": f"{capital_with_interest_and_inflation_and_commision} €",
            "Differenz": f"{round(capital_with_interest_and_inflation - capital_with_interest_and_inflation_and_commision, 2)} €",
            "monatliche Rente privat": f"{round(((capital_with_interest - capital_without_interest) * (1 - TAX_RATE) + capital_without_interest) / MONTHS_IN_RENT * inflation_in_rent, 2)} €",
            "monatliche Rente PR": f"{round(((capital_with_interest_and_commision - capital_without_interest) * (1 - TAX_RATE / 2) + capital_without_interest) / MONTHS_IN_RENT * inflation_in_rent, 2)} €",
            "monatliche Rente BR": f"{round(((capital_with_interest_and_commision_and_reinvestment - capital_without_interest) * (1 - TAX_RATE) + capital_without_interest) / MONTHS_IN_RENT * inflation_in_rent, 2)} €",
        },
    }

print(json.dumps(data, indent=4, ensure_ascii=False))
