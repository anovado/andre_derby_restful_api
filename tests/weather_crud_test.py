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
            if args[0] == app.config['WIO_HOST'] + '/q':
                return MockResponse({'offset': '2', 'longitude': 4.8995, 'timezone': 'Europe/Amsterdam', 'latitude': 52.3824, 'area_code': '0', 'dma_code': '0', 'organization': 'AS15480 Vodafone-Libertel NV', 'country': 'Netherlands', 'ip': '109.39.13.10', 'country_code3': 'NLD', 'continent_code': 'EU', 'country_code': 'NL'}, 200)
            # elif args[0] == app.config['WIO_HOST'] + '/current':
            #     return MockResponse({'data': [{'rh': 34, 'pod': 'd', 'lon': 4.9, 'pres': 1020.97, 'timezone': 'Europe/Amsterdam', 'ob_time': '2020-04-20 10:26', 'country_code': 'NL', 'clouds': 0, 'ts': 1587378370, 'solar_rad': 767.29, 'state_code': '07', 'city_name': 'Amsterdam', 'wind_spd': 6.33731, 'last_ob_time': '2020-04-20T10:01:00', 'wind_cdir_full': 'east-northeast', 'wind_cdir': 'ENE', 'slp': 1020.77, 'vis': 24.1349, 'h_angle': -12.9, 'sunset': '18:48', 'dni': 882.22, 'dewpt': -1.8, 'snow': 0, 'uv': 6.31723, 'precip': 0, 'wind_dir': 73, 'sunrise': '04:28', 'ghi': 767.29, 'dhi': 113.13, 'aqi': 53, 'lat': 52.38, 'weather': {'icon': 'c01d', 'code': '800', 'description': 'Clear sky'}, 'datetime': '2020-04-20:10', 'temp': 13.9, 'station': 'D3248', 'elev_angle': 44.67, 'app_temp': 13.9}], 'count': 1}, 200)
        else:
            return MockResponse(None, 404)
        
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_check_weather_ip(self, get_mock, client):
        token = create_token()
        res = client.get('/weather/ip',
                         query_string={'ip':"192.92.0.0"},
                         headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
