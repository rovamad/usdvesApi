from service.budaService import budaService as buda
from service.localbitcoinsService import localbitcoinsService as localbit
from flask import jsonify

class exchangeRateService:

	@classmethod
	def calculator(self, bankList, minAmount):
		budaPrice = buda.budaPrice()

		page = 1
		json = localbit.getVESPage(page)
		if 'data' in json:
			ad_list = json['data']['ad_list']
			pagination = json['pagination']

			while 'next' in pagination:
				next_page = localbit.nextPage(ad_list, pagination, page)

				next_ad_list = next_page['ad_list']

				if len(ad_list) < len(next_ad_list):
					ad_list = next_ad_list

				pagination = next_page['pagination']
				page = next_page['page']

			result = []
			for bank in bankList:
				bankListPrice = localbit.createBankList(bank, minAmount, ad_list)
				if (bankListPrice != None):
					result.append({ bank: float(bankListPrice) / float(budaPrice) })

			return jsonify(result)