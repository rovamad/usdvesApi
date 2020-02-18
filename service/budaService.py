import requests

class budaService:

	@classmethod
	def budaPrice(self):
		market = 'btc-clp'
		url = f'https://www.buda.com/api/v2/markets/{market}/quotations'

		amount = 0.1
		response = requests.post(url, json={
			'type': 'bid_given_size',
			'amount': amount,
		})

		response_json = response.json()
		price = (float(response_json['quotation']['quote_exchanged'][0]) / amount) * 1.012
		print('Buda.com BTC in CLP price is ' + str(price))

		return price
