from unittest import mock
from unittest.mock import patch
from . import app, client, cache, create_token, init_database
import json

class TestAmazon():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['X_URL']:
                return MockResponse({
                            "ASIN": "B07JN5SQSQ",
                            "title": "Crocs Women's Classic Tie Dye Graphic Clog, White/Multi, 9 US Women / 7 US Men",
                            "price": "$29.99",
                            "listPrice": "",
                            "imageUrl": "https://m.media-amazon.com/images/I/31A68kTiVcL._SL160_.jpg",
                            "detailPageURL": "https://www.amazon.com/dp/B07JN5SQSQ",
                            "rating": "4.8",
                            "totalReviews": "2600",
                            "subtitle": "",
                            "isPrimeEligible": "1",
                            "converted_price": "24.10 GBP"
                        }, 200)
           
        else:
            return MockResponse(None, 404)
        
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_check_product(self, get_mock, client):
        token = create_token()
        res = client.get('/amazon/price',
                         query_string={'keywords':"bike", 'marketplace':"US"},
                         headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
