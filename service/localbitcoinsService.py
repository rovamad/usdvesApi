import requests
import datetime as dt
import pytz

class localbitcoinsService:
	url = 'https://localbitcoins.com/es/sell-bitcoins-online/ves/.json'

	@classmethod
	def getVESPage(self, pageNumber ):
		args = { 'page': pageNumber }
		response = requests.get(self.url, args)

		if response.status_code == 200:
			response_json = response.json()
		
		return response_json

	@classmethod
	def nextPage(self, ad_list, pagination, page):

			page = page + 1
			json = self.getVESPage(page)
			ad_list = ad_list + json['data']['ad_list']
			
			return {
			'ad_list': ad_list, 
			'pagination': json['pagination'], 
			'page': page
			}

	@classmethod
	def createBankList(self, bank_name, min_amount, ad_list):

			temp_price = 0
			now = dt.datetime.now(pytz.utc)

			for ad in ad_list:

				date_time_str = ad['data']['profile']['last_online'].replace('T',' ').split('+',1)[0]
				date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

				timezone = pytz.utc
				timezone_date_time_obj = timezone.localize(date_time_obj)

				difference = now - timezone_date_time_obj
				duration_in_s = difference.total_seconds() 
				minutes = divmod(duration_in_s, 60)[0]

				if bank_name in ad['data']['bank_name'] and min_amount >= int(ad['data']['min_amount']) and temp_price < int(float(ad['data']['temp_price'])) and minutes <= 30:
					temp_price = ad['data']['temp_price']
			
					return temp_price
