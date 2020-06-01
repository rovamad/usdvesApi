from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
sys.path.insert(0, './service/')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.ExchangeRateService import ExchangeRateService

# Create the application instance
app = Flask(__name__)
api = Api(app)

class ExchangeRateController(Resource):

    # Create a URL route in our application for "/"
    @classmethod
    @app.route('/exchangerate', methods = ["GET"])
    def exchangeRate():

        bankList = ['Banesco', 'Mercantil', 'BOD', 'Provincial']
        minAmount = request.args.get('minAmount')
        market = request.args.get('market')

        return ExchangeRateService.calculator(bankList, minAmount, market)

    @classmethod
    @app.route('/ppbrates', methods = ["GET"])
    def ppbRate():
        
        bankList = ['Banesco', 'Mercantil', 'BOD', 'Provincial']
        marketList = ['clp', 'cop', 'pen']

        return ExchangeRateService.ppbrates(bankList, marketList)

if __name__ == '__main__':
    app.run(debug=True)
