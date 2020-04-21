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
  
    def post(self, template):
    
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
                "Name": "Derby Prayogo",
              },
              "To": [
                {
                "Email": args['email'],
                "Name": args['name'],
                }
              ],
              "Subject": "Recommendation of Products for Your Holiday's Destination",
              "TextPart": "Information product from Amazon",
              "HTMLPart": template,
              "CustomID": "AppGettingStartedTest"
            }
          ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())

api.add_resource(PostEmail, '/send')
