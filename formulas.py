import pandas as pd
import numpy as np
from sympy import Symbol, solve

################# WEEK 1 #################

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
    return y

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

################# WEEK 2 #################

def bond_price(coupon_rate, y, T, face_value):
    bp = face_value / (1 + y)**T
    for t in range(1, T+1):
        bp += coupon_rate * face_value / (1 + y)**t
    return bp

def duration(y, T, face_value, coupon_rate, coupon_payment=0):
    """
    To use coupon_rate: just enter coupon_rate, leaving coupon_payment=0 as default
    To use coupon_payment: set coupon_rate=False, then enter coupon_payment
    """
    if coupon_payment:
        bp = annuity_factor(y, T) * coupon_payment
    else:    
        bp = bond_price(coupon_rate, y, T, face_value)
        coupon_payment = coupon_rate * face_value
    D = T * face_value / (1 + y)**T / bp
    for t in range(1, T+1):
        D += (t * (coupon_payment / (1 + y)**t / bp))
    return D

def duration_convex_table(y, T, face_value, coupon_rate, coupon_payment=0):
    """
    To use coupon_rate: just enter coupon_rate, leaving coupon_payment=0 as default
    To use coupon_payment: set coupon_rate=False, then enter coupon_payment
    """
    if coupon_payment:
        bp = annuity_factor(y, T) * coupon_payment
    else:
        bp = bond_price(coupon_rate, y, T, face_value)
        coupon_payment = coupon_rate * face_value
    dct = {'t': range(1, T + 1),
           'CF': [coupon_payment] * T}
    dct['CF'][-1] += face_value
    df = pd.DataFrame(dct)
    df['PV'] = df['CF'] / (1 + y) ** df['t']
    df['weight'] = df['CF'] / (1 + y) ** df['t'] / bp
    df['t*weight'] = df['t'] * df['weight']
    df['t^2+t'] = df['t'] ** 2 + df['t']
    df['PV*(t^2+t)'] = df['PV'] * df['t^2+t']
    D = df['t*weight'].sum()
    convexity = df['PV*(t^2+t)'].sum() / (df['PV'].sum() * (1 + y) ** 2)
    df =df.append({
                  't': 'TOTAL',
                  'CF': df['CF'].sum(),
                  'PV': df['PV'].sum(),
                  'weight': df['weight'].sum(),
                  't*weight': df['t*weight'].sum(),
                  'PV*(t^2+t)': df['PV*(t^2+t)'].sum()
                  }, ignore_index=True)
    return df, D, convexity
    
def portfolio_weights(duration_liability, duration_a, duration_b):
    """
    returns w, 1-w (w_a, w_b, respectively)
    """
    w = (duration_liability - duration_b) / (duration_a - duration_b)
    return w, 1 - w

def portfolio_amount(duration_liability, duration_a, duration_b, pv_liability=1):
    w_a, w_b = portfolio_weights(duration_liability, duration_a, duration_b)
    amount_a, amount_b = w_a * pv_liability, w_b * pv_liability
    return w_a, w_b, amount_a, amount_b

################# WEEK 3 #################

def covariance(coef, std_1, std_2):
    return coef * std_1 * std_2

def cov_finder(kwargs_dct, std_1, std_2):
    assert len(kwargs_dct) == 1
    for key, value in kwargs_dct.items():
        if key == 'cov':
            cov = value
        elif key == 'coef':
            cov = covariance(value, std_1, std_2)
        break
    return cov

def portfolio_return_two_assets(w1, w2, er_1, er_2):
    return w1 * er_1 + w2 * er_2

def portfolio_risk_two_assets(w1, w2, std_1, std_2, **kwargs):
    cov = cov_finder(kwargs, std_1, std_2)
    variance = w1**2 * std_1**2 + w2**2 * std_2**2 + 2 * w1 * w2 * cov
    return variance ** 0.5

def weights_markowitz_minimum_variance(std_1, std_2, **kwargs):
    cov = cov_finder(kwargs, std_1, std_2)
    w1 = (std_2**2 - cov) / (std_1**2 + std_2**2 - 2 * cov)
    w2 = 1 - w1
    return w1, w2
        
def weights_markowitz_optimal_two_risky(A, er_1, er_2, std_1, std_2, coef):
    w1 = (er_1 - er_2 + A * (std_2**2 - std_1 * std_2 * coef)) / (A * (std_1**2 + std_2**2 - 2 * std_1 * std_2 * coef))
    w2 = 1 - w1
    return w1, w2

def weights_markowits_optimal_two_riksy_one_free(eR_1, eR_2, std_1, std_2, **kwargs):
    cov = cov_finder(kwargs, std_1, std_2)
    w1 = (eR_1 * std_2**2 - eR_2 * cov) / (eR_1 * std_2**2 + eR_2 * std_1**2 - (eR_1 + eR_2) * cov)
    w2 = 1 - w1
    return w1, w2

##########################################

if __name__ == '__main__':
    print('All Functions Loaded.')
    # print(duration_convex_table(0.07, 10, 1000, 0.07))
    # print(duration_convex_table(0.08, 10, 1000, 0.07))
    print(portfolio_risk_two_assets(0.5, 0.5, 0.1, 0.2, coef=0.8))
    print(weights_markowitz_minimum_variance(0.2, 0.354, cov=0.1))