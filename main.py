import requests
import datetime as dt
import pytz

url = 'https://localbitcoins.com/es/sell-bitcoins-online/ves/.json'

def getVESPage( pageNumber ):
	args = { 'page': pageNumber }
	response = requests.get(url, args)

	if response.status_code == 200:
		response_json = response.json() #Dic
	
	return response_json

def next(ad_list, pagination, page):

		page = page + 1
		json = getVESPage(page)
		ad_list = ad_list + json['data']['ad_list']
		
		return {
		'ad_list': ad_list, 
		'pagination': json['pagination'], 
		'page': page
		}

def createBankList(bank_name, min_amount, ad_list):

		temp_price = 0;
		now = dt.datetime.now(pytz.utc)
		print('now ', now)

		for ad in ad_list:

			date_time_str = ad['data']['profile']['last_online'].replace('T',' ').split('+',1)[0]
			date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

			timezone = pytz.utc
			timezone_date_time_obj = timezone.localize(date_time_obj)

			difference = now - timezone_date_time_obj
			seconds_in_day = 24 * 60 * 60
			duration_in_s = difference.total_seconds() 
			minutes = divmod(duration_in_s, 60)[0]

			#divmod(difference.days * seconds_in_day + difference.seconds, 60)
			#test = datetime.mktime(difference)
			#minutes = int(test) / 60 % 60
			# print('minutes ', minutes)
			# print('type ', type(minutes))

			# print('30 ', 30)
			# print('type ', type(30))

			if bank_name in ad['data']['bank_name'] and min_amount >= int(ad['data']['min_amount']) and temp_price < int(float(ad['data']['temp_price'])) and minutes <= 30:
				temp_price = ad['data']['temp_price']
		
				return temp_price

page = 1
json = getVESPage(page)
if 'data' in json:
	ad_list = json['data']['ad_list']
	pagination = json['pagination']

	while 'next' in pagination:
		next_page = next(ad_list, pagination, page)

		next_ad_list = next_page['ad_list']

		if len(ad_list) < len(next_ad_list):
		 	ad_list = next_ad_list

		pagination = next_page['pagination']
		page = next_page['page']

	bod = createBankList('BOD', 10000000, ad_list)

	print('ad_list', len(ad_list))
	print ('bod mayor temp_price', bod)
