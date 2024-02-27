from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

def get_conversion_amount():
    while True:
        try: 
            amount = round(float(request.form['amount']), 2)
            if amount <= 0:
                print("Por favor, digite um número positivo.")
            else:
                return amount
        except ValueError:
            print("Por favor, digite um número válido.")

def convert_to_currency(amount, currency):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'id': '13502',  # ID da worldcoin
        'convert': currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '16adc406-9d25-466d-bfc4-2e34d3e7f469',
    }

    try:
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()
        price = data['data']['13502']['quote'][currency]['price']
        converted_amount = round(amount * price, 2)
        return converted_amount
    except Exception as e:
        print(e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    amount_wld = get_conversion_amount()
    one_wld_usd = round(convert_to_currency(1, 'USD'), 2)
    one_wld_eur = round(convert_to_currency(1, 'EUR'), 2)
    converted_usd = round(convert_to_currency(amount_wld, 'USD'), 2)
    converted_eur = round(convert_to_currency(amount_wld, 'EUR'), 2)

    if converted_usd is not None and converted_eur is not None:
        final_price_usd_75 = round(converted_usd * 0.75, 2)
        final_price_usd_80 = round(converted_usd * 0.80, 2)
        final_price_eur_75 = round(converted_eur * 0.75, 2)
        final_price_eur_80 = round(converted_eur * 0.80, 2)
        final_price_eur_75_profit = round(converted_eur * 0.25, 2)
        final_price_eur_80_profit = round(converted_eur * 0.20, 2)
        return render_template('result.html', amount_wld=amount_wld, converted_usd=converted_usd, converted_eur=converted_eur, one_wld_usd=one_wld_usd, one_wld_eur=one_wld_eur, final_price_usd_75=final_price_usd_75, final_price_usd_80=final_price_usd_80, final_price_eur_75=final_price_eur_75, final_price_eur_80=final_price_eur_80, final_price_eur_75_profit=final_price_eur_75_profit, final_price_eur_80_profit=final_price_eur_80_profit)
    else:
        return "Erro na conversão"

@app.route('/back')
def back():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
