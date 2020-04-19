from mailjet_rest import Client
import requests, config, os
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from blueprints import app
from blueprints.amazon.resources import GetPriceReport


bp_email = Blueprint('email', __name__)
api = Api(bp_email)

class PostEmail(Resource):
    # url = 
  
    def Post(self):
        getprice = GetPriceReport()
        returned_data = getprice.get()
        search_result = returned_data[0][0]
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='args', default=None)
        parser.add_argument('email', location='args', default=None)
        args=parser.parse_args()
        
        api_key = app.config['EMAIL_KEY']
        api_secret = app.config['EMAIL_SECRET']

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
          'Messages': [
            {
              "From": {
                "Email": "andrenovado@gmail.com",
                "Name": args['name'],
              },
              "To": [
                {
                "Email": args['email'],
                "Name": args['name'],
                }
              ],
              "Subject": f"Information about {search_result['title']}",
              "TextPart": "Information product from Amazon",
              "HTMLPart": f"<h2>{search_result['title']}</h2><br /><h5>Price: {search_result['price']}</h5><img src='{search_result['imageUrl']}' alt='Product image'><br /><h5>Rating: {search_result['rating']}</h5><h5>Total Reviews: {search_result['totalReviews']}</h5><br /><a href='{search_result['detailPageURL']}''>See more details here...</a>",
              "CustomID": "AppGettingStartedTest"
            }
          ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())

api.add_resource(PostEmail, '/send')
