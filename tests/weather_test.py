from unittest import mock
from unittest.mock import patch
from . import app, client, cache, create_token, init_database
import json

class TestWeather():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['WIO_HOST']:
                return MockResponse({
                    "cod": "200",
                    "message": 0,
                    "cnt": 40,
                    "list": [
                        {
                            "dt": 1587470400,
                            "main": {
                                "temp": 202.4,
                                "feels_like": 306.41,
                                "temp_min": 301.83,
                                "temp_max": 302.4,
                                "pressure": 1009,
                                "sea_level": 1009,
                                "grnd_level": 1008,
                                "humidity": 72,
                                "temp_kf": 0.57
                            },
                            "weather": [
                                {
                                    "id": 500,
                                    "main": "Rain",
                                    "description": "light rain",
                                    "icon": "10n"
                                }
                            ],
                            "clouds": {
                                "all": 69
                            },
                            "wind": {
                                "speed": 2.31,
                                "deg": 62
                            },
                            "rain": {
                                "3h": 1.57
                            },
                            "sys": {
                                "pod": "n"
                            },
                            "dt_txt": "2020-04-21 12:00:00"
                        }]}, 200)
           
        else:
            return MockResponse(None, 404)
    
    def mocked_requests_get2(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['WIO_HOST']:
                return MockResponse({
                    "cod": "200",
                    "message": 0,
                    "cnt": 40,
                    "list": [
                        {
                            "dt": 1587470400,
                            "main": {
                                "temp": 302.4,
                                "feels_like": 306.41,
                                "temp_min": 301.83,
                                "temp_max": 302.4,
                                "pressure": 1009,
                                "sea_level": 1009,
                                "grnd_level": 1008,
                                "humidity": 72,
                                "temp_kf": 0.57
                            },
                            "weather": [
                                {
                                    "id": 500,
                                    "main": "Rain",
                                    "description": "light rain",
                                    "icon": "10n"
                                }
                            ],
                            "clouds": {
                                "all": 69
                            },
                            "wind": {
                                "speed": 2.31,
                                "deg": 62
                            },
                            "rain": {
                                "3h": 1.57
                            },
                            "sys": {
                                "pod": "n"
                            },
                            "dt_txt": "2020-04-21 12:00:00"
                        }]}, 200)
           
        else:
            return MockResponse(None, 404)
    
    def mocked_requests_get3(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        if len(args) > 0:
            if args[0] == app.config['WIO_HOST']:
                return MockResponse({
                    "cod": "200",
                    "message": 0,
                    "cnt": 40,
                    "list": [
                        {
                            "dt": 1587470400,
                            "main": {
                                "temp": 402.4,
                                "feels_like": 306.41,
                                "temp_min": 301.83,
                                "temp_max": 302.4,
                                "pressure": 1009,
                                "sea_level": 1009,
                                "grnd_level": 1008,
                                "humidity": 72,
                                "temp_kf": 0.57
                            },
                            "weather": [
                                {
                                    "id": 500,
                                    "main": "Rain",
                                    "description": "light rain",
                                    "icon": "10n"
                                }
                            ],
                            "clouds": {
                                "all": 69
                            },
                            "wind": {
                                "speed": 2.31,
                                "deg": 62
                            },
                            "rain": {
                                "3h": 1.57
                            },
                            "sys": {
                                "pod": "n"
                            },
                            "dt_txt": "2020-04-21 12:00:00"
                        }]}, 200)
           
        else:
            return MockResponse(None, 404)
        
           
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_check_weather(self, get_mock, client):
        token = create_token()
        res = client.get('/weather/q',
                         query_string={'city':"london"},
                         headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    @mock.patch('requests.get', side_effect=mocked_requests_get2)
    def test_check_weather2(self, get_mock, client):
        token = create_token()
        res = client.get('/weather/q',
                         query_string={'city':"london"},
                         headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    @mock.patch('requests.get', side_effect=mocked_requests_get3)
    def test_check_weather3(self, get_mock, client):
        token = create_token()
        res = client.get('/weather/q',
                         query_string={'city':"london"},
                         headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200

    