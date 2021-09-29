import requests

class BudaService:

    @classmethod
    def budaPrice(self, market):
        market = f'btc-{market}'
        url = f'https://www.buda.com/api/v2/markets/{market}/quotations'

        amount = 0.1
        price = 999999999999999

        try:
            response = requests.post(url, json={
                'type': 'bid_given_size',
                'amount': amount
            })

            if response.status_code == 201:
                response_json = response.json()
                price = (float(response_json['quotation']['quote_exchanged'][0]) / amount) * 1.012
                print('Buda.com BTC in ' + market + ' price is ' + str(price))
        
        except requests.exceptions.RequestException as e:
            print('Error getting Buda.com price')
            print(e.args)

        return price
