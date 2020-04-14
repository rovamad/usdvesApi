from service.budaService import budaService as buda
from service.localbitcoinsService import localbitcoinsService as localbit
from flask import jsonify

class exchangeRateService:

	@classmethod
	def calculator(self, bankList, minAmount, market):
		budaPrice = buda.budaPrice(market)
		localMarketPrice = localbit.getLocalMarketPage(market)
		print('Localbitcoin BTC in ' + market +' price is ' + str(localMarketPrice))
		betterPrice = localMarketPrice
		source = f'Localbitcoins {market}'

		if float(budaPrice) < float(localMarketPrice):
			betterPrice = budaPrice
			source = f'Buda.com btc-{market}'

		print('betterPrice is ' + str(betterPrice))
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
			bankPriceAcumulator = 0
			bankFound = 0
			for bank in bankList:
				bankListPrice, specific_ad = localbit.createBankList(bank, minAmount, ad_list)
				if (bankListPrice != None):
					bankFound = bankFound + 1
					rate = float(bankListPrice) / float(betterPrice)
					result.append({ bank : rate,
					'ad': specific_ad})
					bankPriceAcumulator = (float(bankPriceAcumulator) + float(rate))
			
			print('bankPriceAcumulator' + str(bankPriceAcumulator))
			print('bankFound' + str(bankFound))
			bankPriceAverage = bankPriceAcumulator / bankFound

			return jsonify(betterPrice=betterPrice,
			source=source,
			average=bankPriceAverage,
			banks=result)