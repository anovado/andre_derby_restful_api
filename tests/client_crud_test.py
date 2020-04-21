import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestClientCrud():
    def test_client_list(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_client(self, client, init_database):
        token = create_token()
        res = client.get('/client/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_not_found(self, client, init_database):
        token = create_token()
        res = client.get('/client/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    
    def test_post_client(self, client, init_database):
        token = create_token()
        data={
                "client_key":"tes",
                "client_secret":"tes"
        }
        res = client.post('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_put_client(self, client, init_database):
        token = create_token()
        data={
                "client_key":"tes",
                "client_secret":"tes"
        }
        res = client.put('/client/1',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_put_client_not_found(self, client, init_database):
        token = create_token()
        data={
                "client_key":"tes",
                "client_secret":"tes"
        }
        res = client.put('/client/100',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_delete_client(self, client, init_database):
        token = create_token()
        res = client.delete('/client/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_client_not_found(self, client, init_database):
        token = create_token()
        res = client.delete('/client/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_client_by_id(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'id':1},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_client_by_status(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'status':"true"},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_client_sort_desc_id(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'id', 'sort':'desc'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_client_sort_id(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'id'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_client_sort_status(self, client, init_database):
        token = create_token()
        res = client.get('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'status'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_patch_client(self, client, init_database):
        token = create_token()
        res = client.patch('/client',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 501