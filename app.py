from flask import Flask, render_template, request, url_for
from formulas import *

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def main_get(num=None):
    return render_template('index.html', num=num)

# @app.route('/calc_cur_yield', methods=['POST', 'GET'])
# def calc_cur_yield(num=None):
#     if request.method == 'POST':
#         pass
#     elif request.method == 'GET':
#     # get user inputs
#         annual_coupon = request.args.get('annual_coupon')
#         annual_coupon = float(annual_coupon)
#         bond_price = request.args.get('bond_price')
#         bond_price = float(bond_price)
#         # calculate
#         result = current_yield(annual_coupon, bond_price)
#         return render_template('index.html', result1 = result)

# @app.route('/calc_eay', methods=['POST', 'GET'])
# def calc_eay(num=None):
#     if request.method == 'POST':
#         pass
#     elif request.method == 'GET':
#     # get user inputs
#         i = request.args.get('i')
#         i = float(i)
#         days = request.args.get('days')
#         days = int(days)
#         # calculate
#         result = effective_annual_yield(i, days)
#         result = 'Result: ' + str(result)
#         return render_template('index.html', result2 = result)

@app.route('/calc_yield_to_maturity', methods=['POST', 'GET'])
def calc_yield_to_maturity(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
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
            result = 'Result: ' + str(result)
        except:
            result = 'ERROR: Wrong Value'
        return render_template('index.html', result3 = result)

@app.route('/calc_ytm_to_fr', methods=['POST', 'GET'])
def calc_ytm_to_fr(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            ytm_lst = request.args.get('ytm_lst')
            ytm_lst = list(map(float, ytm_lst.split(',')))
            df = ytm_to_fr(ytm_lst)
            result = df.to_html(classes='data')
            return render_template('index.html', tables=[result], 
                                titles=df.columns.values)
        except:
            return render_template('index.html', result4='ERROR: Wrong Value')

@app.route('/calc_prices_to_ytm_fr', methods=['POST', 'GET'])
def calc_prices_to_ytm_fr(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            price_lst = request.args.get('price_lst')
            price_lst = list(map(float, price_lst.split(',')))
            df = prices_to_ytm_fr(price_lst)
            result = df.to_html(classes='data')
            return render_template('index.html', tables2=[result])
        except:
            return render_template('index.html', result5='ERROR: Wrong Value')

if __name__ == '__main__':
    # 외부 접속용
    # app.run(host='192.168.50.24', debug=True)
    # 로컬 전용
    app.run(debug=True)
