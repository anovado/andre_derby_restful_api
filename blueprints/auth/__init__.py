from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

import hashlib, uuid
from blueprints import internal_required
from ..client.model import Clients

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

### Resources

class CreateTokenResource(Resource):
    
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args',required=True)
        parser.add_argument('client_secret',location='args', required=True)
        args = parser.parse_args()
        
        qry = Clients.query.filter_by(client_key=args['client_key']).first()
        if qry is not None:
            encoded = ('%s%s' % (args['client_secret'], qry.salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            
            if hash_pass == qry.client_secret:
                qry = marshal(qry, Clients.jwt_claims_fields)
                qry['identifier'] = 'amazon project'
                # qry['status'] = False
                token = create_access_token(identity=args['client_key'], user_claims=qry)
                return {'token':token}, 200
            
        if args['client_key'] == 'internal' and args['client_secret'] == 'super_secret_client':
            qry = {
                'identifier': 'amazon project',
                'status': True
            }
            token = create_access_token(identity=args['client_key'], user_claims=qry)
            return {'token':token}, 200
        else:
            return  {'status':'UNAUTHORIZED', 'message': 'invalid key or secret'}, 404
    

class RefreshTokenResource(Resource):
    
    @internal_required
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt_claims()
        token = create_access_token(identity=current_user, user_claims=claims)
        return {'token':token, 'claims':claims}, 200
    

api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')