import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required

bp_conversion = Blueprint('conversion', __name__)
api = Api(bp_conversion)

class GetConversion(Resource):
    url = "https://currency-value.p.rapidapi.com/global/currency_rates"

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('currency', location='args', default=None)
        args=parser.parse_args()
        payload = "{\n\t\"from\": \"USD\",\n    \"to\": \"HKD\"\n}"
        headers = {
            'x-rapidapi-host': 'currency-value.p.rapidapi.com',
            'x-rapidapi-key': '5f6997638bmsh0072972d1fcfa8bp129664jsn47872153a2b4',
            'Content-Type': 'application/json'
        }
        response = requests.request("GET", self.url, headers=headers, data = payload)
        data = response.json()
        price = 512412
        data_list = data['currency_rates']
        rows = []
        for _, (ky, val) in enumerate(data_list.items()) :
            if ky == args['currency']:
                rows.append('%s => %f' % (ky, price*data['currency_rates']['IDR']/val))

        return rows, 200

api.add_resource(GetConversion, '/con')
