from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
sys.path.insert(0, './service/')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.exchangeRateService import exchangeRateService

# Create the application instance
app = Flask(__name__)
api = Api(app)

class ExchangeRateController(Resource):

    # Create a URL route in our application for "/"
    # def get(self):
    @classmethod
    @app.route('/exchangerate', methods = ["GET"])
    def exchangeRate():
        """
        This function just responds to the browser ULR
        localhost:5000/

        :return:        the rendered template 'home.html'
        """
        bankList = ['Banesco', 'Mercantil', 'BOD', 'Provincial']
        minAmont = request.args.get('minAmont')
        market = request.args.get('market')

        return exchangeRateService.calculator(bankList, minAmont, market)

# api.add_resource(ExchangeRateController, '/clpves') # Route_1

if __name__ == '__main__':
    app.run(debug=True)
