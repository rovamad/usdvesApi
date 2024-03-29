import requests
import datetime as dt
import pytz

class LocalbitcoinsService:

    @classmethod
    def getVEDPage(self, pageNumber ):
        url = 'https://localbitcoins.com/es/vender-bitcoins-online/ved/.json'
        args = { 'page': pageNumber }
        response = requests.get(url, args)

        if response.status_code == 200:
            response_json = response.json()
        
        return response_json

    @classmethod
    def nextPage(self, ad_list, pagination, page):

            page = page + 1
            json = self.getVEDPage(page)
            ad_list = ad_list + json['data']['ad_list']
            
            return {
            'ad_list': ad_list, 
            'pagination': json['pagination'], 
            'page': page
            }

    @classmethod
    def createBankList(self, bank_name, min_amount, ad_list):

        temp_price = 0
        specific_ad = ''
        now = dt.datetime.now(pytz.utc)

        for ad in ad_list:

            date_time_str = ad['data']['profile']['last_online'].replace('T',' ').split('+',1)[0]
            date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            timezone = pytz.utc
            timezone_date_time_obj = timezone.localize(date_time_obj)

            difference = now - timezone_date_time_obj
            duration_in_s = difference.total_seconds() 
            minutes = divmod(duration_in_s, 60)[0]

            if ad['data']['min_amount'] != None and ad['data']['max_amount_available'] != None and \
                bank_name in ad['data']['bank_name'] and \
                float(ad['data']['min_amount']) <= float(min_amount) <= float(ad['data']['max_amount_available']) and \
                float(temp_price) < float(ad['data']['temp_price']) and minutes <= 30 and \
                int(ad['data']['profile']['feedback_score']) > 95 and \
                (ad['data']['online_provider']=='SPECIFIC_BANK' or ad['data']['online_provider'] =='NATIONAL_BANK'):
                
                    temp_price = ad['data']['temp_price']
                    specific_ad = ad['actions']['public_view']
        
        return temp_price, specific_ad

    @classmethod
    def getLocalMarketPage(self, market):
        url = f'https://localbitcoins.com/buy-bitcoins-online/{market}/.json'
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
                    country_amount = 300000
                    if market.casefold() == "pen":
                        country_amount = 100

                    if float(ad['data']['temp_price']) < float(temp_price) and \
                        ad['data']['min_amount'] != None and \
                        ad['data']['max_amount_available'] != None and \
                        float(ad['data']['min_amount']) <= country_amount <= float(ad['data']['max_amount_available']) and \
                        minutes <= 30 and int(ad['data']['profile']['feedback_score']) > 95 and \
                        (ad['data']['online_provider']=='SPECIFIC_BANK' or ad['data']['online_provider'] =='NATIONAL_BANK'):
                            temp_price = ad['data']['temp_price']
        
                return temp_price

