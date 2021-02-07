from flask import Flask, render_template, request, url_for
from formulas import *

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def main_get(num=None):
    return render_template('index.html', num=num)

@app.route('/calc_cur_yield', methods=['POST', 'GET'])
def calc_cur_yield(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
    # get user inputs
        annual_coupon = request.args.get('annual_coupon')
        annual_coupon = float(annual_coupon)
        bond_price = request.args.get('bond_price')
        bond_price = float(bond_price)
        # calculate
        result = current_yield(annual_coupon, bond_price)
        return render_template('index.html', result1 = result)

@app.route('/calc_eay', methods=['POST', 'GET'])
def calc_eay(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
    # get user inputs
        i = request.args.get('i')
        i = float(i)
        days = request.args.get('days')
        days = int(days)
        # calculate
        result = effective_annual_yield(i, days)
        return render_template('index.html', result2 = result)

@app.route('/calc_yield_to_maturity', methods=['POST', 'GET'])
def calc_yield_to_maturity(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        # get user inputs
        T = request.args.get('T')
        T = int(T)
        C = request.args.get('C')
        C = float(C)
        bond_price = request.args.get('bond_price')
        bond_price = float(bond_price)
        face_value = request.args.get('face_value')
        face_value = float(face_value)
        # calculate
        result = yield_to_maturity(T, C, bond_price, face_value)
        return render_template('index.html', result3 = result)

@app.route('/calc_ytm_to_fr', methods=['POST', 'GET'])
def calc_ytm_to_fr(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        ytm_lst = request.args.get('ytm_lst')
        ytm_lst = list(map(float, ytm_lst.split(',')))
        df = ytm_to_fr(ytm_lst)
        result = df.to_html(classes='data')
        return render_template('index.html', tables=[result], 
                               titles=df.columns.values)

@app.route('/calc_prices_to_ytm_fr', methods=['POST', 'GET'])
def calc_prices_to_ytm_fr(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        price_lst = request.args.get('price_lst')
        price_lst = list(map(float, price_lst.split(',')))
        df = prices_to_ytm_fr(price_lst)
        result = df.to_html(classes='data')
        return render_template('index.html', tables2=[result])

if __name__ == '__main__':
    app.run(debug=True)

