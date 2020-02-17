import requests
import datetime as dt
import pytz

class localbitcoinsService:

	@classmethod
	def getVESPage(self, pageNumber ):
		url = 'https://localbitcoins.com/es/sell-bitcoins-online/ves/.json'
		args = { 'page': pageNumber }
		response = requests.get(url, args)

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

			if ad['data']['min_amount'] != None and ad['data']['max_amount'] != None and bank_name in ad['data']['bank_name'] and min_amount >= int(ad['data']['min_amount']) and float(temp_price) < float(ad['data']['temp_price']) and minutes <= 30:
				temp_price = ad['data']['temp_price']
		
		return temp_price

	@classmethod
	def getCLPPage(self):
		url = 'https://localbitcoins.com/buy-bitcoins-online/clp/.json'
		page = 1
		args = { 'page': page }
		response = requests.get(url, args)

		if response.status_code == 200:
			response_json = response.json()

			if 'data' in response_json:
				ad_list = response_json['data']['ad_list']

				temp_price = 999999999999999999999
				now = dt.datetime.now(pytz.utc)

				for ad in ad_list:

					date_time_str = ad['data']['profile']['last_online'].replace('T',' ').split('+',1)[0]
					date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

					timezone = pytz.utc
					timezone_date_time_obj = timezone.localize(date_time_obj)

					difference = now - timezone_date_time_obj
					duration_in_s = difference.total_seconds() 
					minutes = divmod(duration_in_s, 60)[0]

					if float(ad['data']['temp_price']) < float(temp_price) and ad['data']['min_amount'] != None and ad['data']['max_amount'] != None and float(ad['data']['min_amount']) <= 300000 <= float(ad['data']['max_amount']) and minutes <= 30 and int(ad['data']['profile']['feedback_score']) > 95:
						if ad['data']['online_provider']=='SPECIFIC_BANK' or ad['data']['online_provider'] =='NATIONAL_BANK':
							temp_price = ad['data']['temp_price']
		
				return temp_price
