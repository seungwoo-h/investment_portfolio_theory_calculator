import pandas as pd
import numpy as np
from sympy import Symbol, solve

def current_yield(annual_coupon, bond_price):
    return annual_coupon / bond_price

def effective_annual_yield(i, days):
    return (1 + i) ** (365 / days) - 1

def yield_to_maturity(T, C, bond_price, face_value):
    y = Symbol('y')
    equation = face_value / (1 + y) ** T - bond_price
    for t in range(1, T + 1):
        equation += C / (1 + y) ** t
    y = solve(equation, y)
    return y[0]

def realized_compound_return(V_T, V_0, T):
    return (V_T / V_0) ** (1 / T) - 1

def annuity_factor(r, T):
    return (1 / r) * (1 - 1 / (1 + r) ** T)

def pv_factor(r, T):
    return 1 / (1 + r) ** T

def holding_period_return(coupon_income, sale_price, purchase_price):
    """
    HPR
    """
    return (coupon_income + sale_price - purchase_price) / purchase_price

def forward_rates(y_now, y_before, n):
    return ((1 + y_now) ** n / (1 + y_before) ** (n - 1)) - 1

def prices_to_ytm_fr(price_of_bonds):
    prices_dct = dict()
    prices_dct['maturity'] = range(1, len(price_of_bonds)+1)
    prices_dct['price_of_bond'] = price_of_bonds
    df = pd.DataFrame(prices_dct)
    
    df['YtM'] = np.NaN
    df['YtM'] = df.apply(lambda x: round((1000 / df['price_of_bond']) ** (1/df['maturity']) - 1, 4))
    
    df['forward_rate'] = df['YtM'][0]
    for i in range(len(df)):
        if i == 0:
            continue
        y_now = df['YtM'][i]
        y_before = df['YtM'][i-1]
        n = i + 1
        df['forward_rate'][i] = round(forward_rates(y_now, y_before, n), 3)
    
    return df

def ytm_to_fr(ytms):
    df = pd.DataFrame({'Maturity': range(1, len(ytms) + 1), 'YtM': ytms})
    df['forward_rate'] = df['YtM'][0]
    for i in range(len(df)):
        if i == 0:
            continue
        y_now = df['YtM'][i]
        y_before = df['YtM'][i-1]
        n = i + 1
        df['forward_rate'][i] = round(forward_rates(y_now, y_before, n), 3)
    return df