import requests, config
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from blueprints import app
from blueprints.amazon.resources import GetPriceReport


bp_conversion = Blueprint('conversion', __name__)
api = Api(bp_conversion)

class GetConversion(Resource):
    url = "https://currency-value.p.rapidapi.com/global/currency_rates"

    def get(self):
        getprice = GetPriceReport()
        # parser = reqparse.RequestParser()
        # args=parser.parse_args()
        # amazon_api = GetPriceReport
        returned_data = getprice.get()
        search_result = returned_data[0][0]
        origin_currency = returned_data[1]
        target_currency = returned_data[2]
        # currency = returned_data[1]
        payload = "{\n\t\"from\": \"USD\",\n    \"to\": \"HKD\"\n}"
        headers = {
            'x-rapidapi-host': app.config['HOST_MATAUANG'],
            'x-rapidapi-key': app.config['KEY_MATAUANG'],
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", self.url, headers=headers, data = payload)
        data = response.json()
        price = float(search_result['price'][1:])
        data_list = data['currency_rates']
        # rows = []
        for _, (ky, val) in enumerate(data_list.items()) :
            if ky == target_currency:
                # rows.append('%s => %f' % (ky, price*data['currency_rates'][target_currency]/val))
                search_result['converted_price'] = '%f %s' % (price*data['currency_rates'][origin_currency]/val, target_currency)
        return search_result, 200

api.add_resource(GetConversion, '/con')
