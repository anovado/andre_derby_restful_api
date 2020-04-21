import requests, math
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
from blueprints import app
from blueprints.amazon.resources import GetPriceReport
from blueprints.email.resources import PostEmail

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)

class PublicGetCurrentWeather(Resource):    
    wio_host = app.config['WIO_HOST']
    wio_apikey = app.config['WIO_KEY']
        
    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', location='args', default=None)
        args = parser.parse_args()

        rq = requests.get(self.wio_host, params={'q': args['city'], 'appid': self.wio_apikey})
        geo = rq.json()
        temperature = float(geo['list'][4]['main']['temp']) - 273.15
        search_result=[]
        template =[]
        rounded_temp = math.floor(temperature * 100) / 100
        search_result.append(f"Your destination temperature is {rounded_temp} ° Celcius")
        
        if temperature < 10:
            shirt = GetPriceReport().get('shirt for winter')
            pants = GetPriceReport().get('pants for winter')
            jackets = GetPriceReport().get('jackets for winter')
            shoes = GetPriceReport().get('shoes for winter')
            hat = GetPriceReport().get('hat for winter')
            search_result.append(shirt[0])
            search_result.append(pants[0])
            search_result.append(jackets[0])
            search_result.append(shoes[0])
            search_result.append(hat[0])
            template.append(shirt[1])
            template.append(pants[1])
            template.append(jackets[1])
            template.append(shoes[1])
            template.append(hat[1])
        elif 10 <= temperature < 30:
            shirt = GetPriceReport().get('shirt for fall')
            pants = GetPriceReport().get('pants for fall')
            jackets = GetPriceReport().get('jackets for fall')
            shoes = GetPriceReport().get('shoes for fall')
            hat = GetPriceReport().get('hat for fall')
            search_result.append(shirt[0])
            search_result.append(pants[0])
            search_result.append(jackets[0])
            search_result.append(shoes[0])
            search_result.append(hat[0])
            template.append(shirt[1])
            template.append(pants[1])
            template.append(jackets[1])
            template.append(shoes[1])
            template.append(hat[1])
        elif temperature >= 30:
            shirt = GetPriceReport().get('shirt for summer')
            pants = GetPriceReport().get('pants for summer')
            jackets = GetPriceReport().get('jackets for summer')
            shoes = GetPriceReport().get('shoes for summer')
            hat = GetPriceReport().get('hat for summer')
            search_result.append(shirt[0])
            search_result.append(pants[0])
            search_result.append(jackets[0])
            search_result.append(shoes[0])
            search_result.append(hat[0])
            template.append(shirt[1])
            template.append(pants[1])
            template.append(jackets[1])
            template.append(shoes[1])
            template.append(hat[1])
        template_toprint = ''.join(map(str, template))    
        PostEmail().post(template_toprint)
        return search_result, 200


api.add_resource(PublicGetCurrentWeather, '/q')