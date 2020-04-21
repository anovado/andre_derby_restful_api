import json
from sqlalchemy.sql import func
from . import app, client, cache, create_token, create_token_non_internal, init_database

class TestUserCrud():
    def test_user_list(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user(self, client, init_database):
        token = create_token()
        res = client.get('/user/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_user_not_found(self, client, init_database):
        token = create_token()
        res = client.get('/user/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    
    def test_post_user(self, client, init_database):
        token = create_token()
        data={
                "client_id":1,
                "name":"haha",
                "age":12,
                "sex":"male" 
        }
        res = client.post('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_put_user(self, client, init_database):
        token = create_token()
        data={
                "client_id":1,
                "name":"haha",
                "age":12,
                "sex":"male"
        }
        res = client.put('/user/1',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_put_user_not_found(self, client, init_database):
        token = create_token()
        data={
                "client_id":1,
                "name":"haha",
                "age":12,
                "sex":"male"
        }
        res = client.put('/user/100',
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data),
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_delete_user(self, client, init_database):
        token = create_token()
        res = client.delete('/user/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_user_not_found(self, client, init_database):
        token = create_token()
        res = client.delete('/user/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_user_by_sex(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'sex':"male"},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_user_sort_desc_age(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'age', 'sort':'desc'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_book_sort_age(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'age'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_get_user_sort_desc_sex(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'sex', 'sort':'desc'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_book_sort_sex(self, client, init_database):
        token = create_token()
        res = client.get('/user',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'sex'},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
        