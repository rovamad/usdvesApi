from service.BudaService import BudaService as buda
from service.LocalbitcoinsService import LocalbitcoinsService as localbit
from flask import jsonify

class ExchangeRateService:

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
        json = localbit.getVEDPage(page)
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
                if (bankListPrice != 0 and specific_ad != ''):
                    bankFound = bankFound + 1
                    rate = float(bankListPrice) / float(betterPrice)
                    result.append({ bank : rate,
                    'ad': specific_ad})
                    bankPriceAcumulator = (float(bankPriceAcumulator) + float(rate))
            
            bankPriceAverage = bankPriceAcumulator / bankFound

            return jsonify(
                betterPrice=betterPrice, source=source,
                average=bankPriceAverage, banks=result)

    @classmethod
    def ppbrates(self, bankList, marketList):

        rates = {}
        for market in marketList:

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

                minAmount=70000000
                if (market != 'clp'):
                    minAmount=15000000

                for bank in bankList:
                    bankListPrice, specific_ad = localbit.createBankList(bank, minAmount, ad_list)
                    if (bankListPrice != 0 and specific_ad != ''):
                        bankFound = bankFound + 1
                        rate = float(bankListPrice) / float(betterPrice)
                        result.append({ bank : rate,
                        'ad': specific_ad})
                        bankPriceAcumulator = (float(bankPriceAcumulator) + float(rate))
                
                bankPriceAverage = bankPriceAcumulator / bankFound

                recomended = ''
                if (market == 'clp'):
                    recomended = {
                        '7.5%': round((bankPriceAverage * 0.925),4),
                        '6.5%': round((bankPriceAverage * 0.935),4),
                        '4.5%': round((bankPriceAverage * 0.955), 4),
                        }
                elif (market == 'cop'):
                    colFormat = round((1/(bankPriceAverage * 0.99)),4)
                    recomended = {
                            '9%': round((bankPriceAverage * 0.99), 4),
                            'col format': colFormat,
                            '100.000/colformat': round(100000/colFormat, 4)
                            }
                elif (market == 'pen'):
                    recomended = {
                            '4%': round((bankPriceAverage * 0.96),4)
                            }

                rates[market] = {
                                'average': round((bankPriceAverage),4),
                                'recomended': recomended
                                }
        
        return jsonify(rates)