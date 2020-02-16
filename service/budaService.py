import requests

class budaService:

	@classmethod
	def budaPrice(self):
		market = 'btc-clp'
		url = f'https://www.buda.com/api/v2/markets/{market}/quotations'

		response = requests.post(url, json={
			'type': 'bid_given_size',
			'amount': 1,
		})

		response_json = response.json()
		print(response_json['quotation']['quote_exchanged'][0])

		return response_json['quotation']['quote_exchanged'][0]
