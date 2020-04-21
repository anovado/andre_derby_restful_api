import requests, config
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from blueprints import app
from blueprints.conversion.resources import GetConversion

bp_amazon = Blueprint('amazon', __name__)
api = Api(bp_amazon)

class GetPriceReport(Resource):
    url = "https://amazon-price1.p.rapidapi.com/search"
    # x_host = app.config['x_host']
    # x_apikey = app.config['x_key']

    # response = requests.request("GET", url, headers=headers, params=querystring)

    def get(self, keyword):
        parser = reqparse.RequestParser()
        # parser.add_argument('keywords', location='args', default=None)
        # parser.add_argument('marketplace', location='args', default=None)
        args=parser.parse_args()

        querystring = {"keywords":keyword, "marketplace":"US"}
        headers = {
            # 'x-rapidapi-host': "amazon-price1.p.rapidapi.com",
            # 'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79", 
            'x-rapidapi-host' : app.config['X_HOST'],
            'x-rapidapi-key':  app.config['X_APIKEY'],
            'Content-Type': 'application/json'
        }
        response = requests.request('GET', self.url, headers=headers, params=querystring)
        data = response.json()
        converted_price = GetConversion().get(data[0]['price'])
        data['converted_price'] = converted_price
        
        email_template = f"<h3>{data['title']}</h3><br /><h5>Price: {data['price']}</h5><h5>Converted Price: {data['converted_price']}</h5><img src='{data['imageUrl']}' alt='Product image'><br /><h5>Rating: {data['rating']}</h5><h5>Total Reviews: {data['totalReviews']}</h5><br /><a href='{data['detailPageURL']}''>See more details of this product here</a>"
        
        return [data, email_template]

api.add_resource(GetPriceReport, '/price')
