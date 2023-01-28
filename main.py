import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def get_yearly_rates(amount, currency, converted_currency, amount_of_days):

    #start date
    today_date = datetime.datetime.now()
    date_1year = (today_date - datetime.timedelta(days=1 * amount_of_days))

    #requests
    url = f'https://api.exchangerate.host/timeseries'
    payload = {'base': currency, 'amount': amount, 'start_date': date_1year.date(),
               'end_date': today_date.date()}
    response = requests.get(url, params=payload)
    data = response.json()

    #create a dict to store data:
    currency_history = {}
    rate_history_array = []

    for item in data['rates']:
        current_date = item
        currency_rate = data['rates'][item][converted_currency]

        currency_history[current_date] = [currency_rate]
        rate_history_array.append(currency_rate)

    # Clean Data
    pd_data = pd.DataFrame(currency_history).transpose()
    pd_data.columns = ['Rate']
    pd.set_option('display.max.rows', None)
    print(pd_data)

    #Plot Data
    plt.plot(rate_history_array)
    plt.ylabel(f'{amount} {currency} to {converted_currency}')
    plt.xlabel('Days')
    plt.title(f'Current rate for {amount} {currency} to {converted_currency} is {rate_history_array[-1]}')
    plt.show()


get_yearly_rates(1, 'EUR', 'GBP', 365)
