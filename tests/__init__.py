import pytest 
import logging
import json
import hashlib
import uuid
from sqlalchemy.sql import func
from blueprints import app, cache, db
from flask import Flask, request, json
from blueprints.user.model import Users
from blueprints.client.model import Clients

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()
    
    salt = uuid.uuid4().hex
    encoded = ('%s%s' %("super_secret_client", salt)).encode('utf-8')
    hashpass = hashlib.sha512(encoded).hexdigest()
    encoded2 = ('%s%s' %("alta123", salt)).encode('utf-8')
    hashpass2 = hashlib.sha512(encoded2).hexdigest()
    client_internal = Clients(client_key='internal', client_secret=hashpass, salt=salt, status="True")
    client_noninternal = Clients(client_key='client1', client_secret=hashpass2, salt=salt, status="False")    
    db.session.add(client_internal)
    db.session.add(client_noninternal)
    
    db.session.commit()

    user = Users(client_id=1, name='client', age=11, sex='male')

    db.session.add(user)
    
    db.session.commit()
    
    yield db
    
    db.drop_all()
    
    
def create_token():
    token = cache.get('test-token')
    if token is None:
        data={
            'client_key': 'internal',
            'client_secret': 'super_secret_client'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token

def create_token_non_internal():
    token = cache.get('test-token-non-internal')
    if token is None:
        data={
            'client_key': 'client1',
            'client_secret': 'alta123'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-non-internal', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token