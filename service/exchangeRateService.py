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
                    if (bankListPrice != None):
                        bankFound = bankFound + 1
                        rate = float(bankListPrice) / float(betterPrice)
                        result.append({ bank : rate,
                        'ad': specific_ad})
                        bankPriceAcumulator = (float(bankPriceAcumulator) + float(rate))
                
                bankPriceAverage = bankPriceAcumulator / bankFound

                recomended = ''
                if (market == 'clp'):
                    recomended = {
                        '10%': round((bankPriceAverage * 0.9),4),
                        '8%': round((bankPriceAverage * 0.92),4),
                        '6%': round((bankPriceAverage * 0.94), 4),
                        }
                elif (market == 'cop'):
                    recomended = {
                            '12%': round((bankPriceAverage * 0.88), 4),
                            'col format': round((1/(bankPriceAverage * 0.88)),4)
                            }
                elif (market == 'pen'):
                    recomended = {
                            '5%': round((bankPriceAverage * 0.95),4)
                            }

                rates[market] = {
                                'average': round((bankPriceAverage),4),
                                'recomended': recomended
                                }
        
        return jsonify(rates)