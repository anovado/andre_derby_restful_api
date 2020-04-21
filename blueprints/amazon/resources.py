import requests, config, math, random
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from blueprints import app
from blueprints.conversion.resources import GetConversion

bp_amazon = Blueprint('amazon', __name__)
api = Api(bp_amazon)

class GetPriceReport(Resource):
    url = app.config['X_URL']
    
    def get(self, keyword):
        parser = reqparse.RequestParser()
        args=parser.parse_args()

        querystring = {"keywords":keyword, "marketplace":"US"}
        headers = {
            
            'x-rapidapi-host' : app.config['X_HOST'],
            'x-rapidapi-key':  app.config['X_APIKEY'],
            'Content-Type': 'application/json'
        }
        response = requests.request('GET', self.url, headers=headers, params=querystring)
        data = response.json()
        result_product = data[random.randint(0,3)]
        converted_price = GetConversion().get(result_product['price'])
        result_product['converted_price'] = converted_price
        
        email_template = f"<div style='width: 25rem; border:10px black; border-radius:4px; margin-left: 50px; margin-top:30px;margin-bottom:60px;'><img src='{result_product['imageUrl']}' alt='Product picture'><div style='line-height: 15px;'><h3>{result_product['title']}</h3><p>Price: {result_product['price']}</p><p>Converted Price: {result_product['converted_price']}</p><p>Rating: {result_product['rating']}</p><p>Total Reviews: {result_product['totalReviews']}</p><a href='{result_product['detailPageURL']}'>See more</a></div></div>" 
        
        return [result_product, email_template]

api.add_resource(GetPriceReport, '/price')
