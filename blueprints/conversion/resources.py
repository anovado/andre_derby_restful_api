import requests, config
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from blueprints import app
# from blueprints.amazon.resources import GetPriceReport
# from blueprints.email.resources import PostEmail
import re

bp_conversion = Blueprint('conversion', __name__)
api = Api(bp_conversion)

class GetConversion(Resource):
    url = "https://currency-value.p.rapidapi.com/global/currency_rates"

    @jwt_required
    def get(self, product_price):
        parser = reqparse.RequestParser()
        parser.add_argument('target_currency', location='args', default=None)
        args=parser.parse_args()
    
        target_currency = args['target_currency']
        payload = "{\n\t\"from\": \"USD\",\n    \"to\": \"HKD\"\n}"
        headers = {
            'x-rapidapi-host': app.config['HOST_MATAUANG'],
            'x-rapidapi-key': app.config['KEY_MATAUANG'],
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", self.url, headers=headers, data = payload)
        data = response.json()
        price = float((re.findall("[0-9]+,?.?[0-9]+", product_price))[0].replace(',','.'))

        output = ""
        data_list = data['currency_rates']
        for _, (ky, val) in enumerate(data_list.items()) :
            if ky == target_currency:
                output = '%f %s' % (price*data['currency_rates']['USD']/val, target_currency)
        
        
        return output

api.add_resource(GetConversion, '/con')