from flask import Flask, render_template, request, url_for
from formulas import *

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def main_get(num=None):
    return render_template('index.html', num=num)

# @app.route('/calc_yield_to_maturity', methods=['POST', 'GET'])
# def calc_yield_to_maturity(num=None):
#     if request.method == 'POST':
#         pass
#     elif request.method == 'GET':
#         try:
#             # get user inputs
#             T = request.args.get('T')
#             T = int(T)
#             C = request.args.get('C')
#             C = float(C)
#             bond_price = request.args.get('bond_price')
#             bond_price = float(bond_price)
#             face_value = request.args.get('face_value')
#             face_value = float(face_value)
#             # calculate
#             result = yield_to_maturity(T, C, bond_price, face_value)
#             result = 'Result: ' + str(result)
#         except:
#             result = 'ERROR: Wrong Value'
#         return render_template('index.html', result3 = result)

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

@app.route('/calc_duration_convexity', methods=['POST', 'GET'])
def calc_duration_convexity(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            y_value = request.args.get('y_value')
            y_value = float(y_value)
            T = request.args.get('T')
            T = int(T)
            face_value = request.args.get('face_value')
            face_value = float(face_value)
            c_rate_or_payment = request.args.get('c_rate_or_payment')
            c_rate_or_payment = float(c_rate_or_payment)
            if c_rate_or_payment < 1:
                coupon_rate = c_rate_or_payment
                df, D, C = duration_convex_table(y_value, T, face_value, coupon_rate, coupon_payment=0)
            else:
                coupon_payment = c_rate_or_payment
                df, D, C = duration_convex_table(y_value, T, face_value, coupon_rate=False, coupon_payment=coupon_payment)
            result = df.to_html(classes='data')
            return render_template('index.html', duration='Duration: ' + str(D), 
                                                 convexity='Convexity: ' + str(C), tables3=[result])
        except:
            return render_template('index.html', result6='ERROR: Wrong Value')

@app.route('/calc_p_weights_amount', methods=['POST', 'GET'])
def calc_p_weights_amount(num=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        try:
            d_liability = request.args.get('d_liability')
            d_liability = float(d_liability)
            d_a = request.args.get('d_a')
            d_a = float(d_a)
            d_b = request.args.get('d_b')
            d_b = float(d_b)
            pv_l = request.args.get('pv_l')
            pv_l = float(pv_l)
            w_a, w_b, amount_a, amount_b = portfolio_amount(d_liability, d_a, d_b, pv_l)
            if pv_l == 1:
                result = f'1st Bond Weight: {w_a} \t 2nd Bond Weight: {w_b}'
            else:
                result = f'1st Bond Weight: {w_a} \t 2nd Bond Weight: {w_b} \t 1st Bond Amount: {amount_a} \t 2nd Bond Amount: {amount_b}'
            return render_template('index.html', result7=result)
        except:
            return render_template('index.html', result7='ERROR: Wrong Value')



if __name__ == '__main__':
    # 외부 접속용
    # app.run(host='192.168.50.24', debug=True)
    # 로컬 전용
    # app.run(debug=True)
    # pythonanywhere
    if 'liveconsole' not in gethostname():
        app.run(debug=True)