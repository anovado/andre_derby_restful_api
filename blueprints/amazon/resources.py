import requests, config
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from blueprints import app

bp_amazon = Blueprint('amazon', __name__)
api = Api(bp_amazon)

class GetPriceReport(Resource):
    url = "https://amazon-price1.p.rapidapi.com/search"
    # x_host = app.config['x_host']
    # x_apikey = app.config['x_key']

    # response = requests.request("GET", url, headers=headers, params=querystring)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keywords', location='args', default=None)
        parser.add_argument('marketplace', location='args', default=None)
        parser.add_argument('origin_currency', location='args', default=None)
        parser.add_argument('target_currency', location='args', default=None)
        args=parser.parse_args()
        # payload = "{\n\t\"from\": \"USD\",\n    \"to\": \"HKD\"\n}"
        querystring = {"keywords":args['keywords'],"marketplace":args['marketplace']}
        headers = {
            # 'x-rapidapi-host': "amazon-price1.p.rapidapi.com",
            # 'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79", 
            'x-rapidapi-host' : app.config['X_HOST'],
            'x-rapidapi-key':  app.config['X_APIKEY'],
            'Content-Type': 'application/json'
        }
        response = requests.request('GET', self.url, headers=headers, params=querystring)
        data = response.json()
        
        return [data, args['origin_currency'], args['target_currency']]

api.add_resource(GetPriceReport, '/price')
