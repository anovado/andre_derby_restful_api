from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Users
from sqlalchemy import desc

import hashlib, uuid

from blueprints import db, app, internal_required

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):
    def __init__(self):
        pass
    
    @internal_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_field), 200
        return {'status':'NOT_FOUND'}, 404
    
    @internal_required    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        parser.add_argument('client_id', location='json', required=True)

        args = parser.parse_args()


        user = Users(args['name'],args['age'],args['sex'],args['client_id'])
        db.session.add(user)
        db.session.commit()
        app.logger.debug('DEBUG: %s', user)

        return marshal(user, Users.response_field), 200, {'Content-Type': 'application/json'}

    @internal_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        # parser.add_argument('client_id', location='json', required=True)

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        args = parser.parse_args()

        qry.name = args['name']
        qry.age = args['age']
        qry.sex = args['sex']
        # qry.client_id = args['client_id']
        db.session.commit()

        return marshal(qry, Users.response_field), 200, {'Content-Type': 'application/json'}

    @internal_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()
        
        return {'status': 'DELETED'}, 200

class UserList(Resource):
    def __init__(self):
        pass

    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('sex', location='args', help='invalid status', choices=('male', 'female'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('age', 'sex'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Users.query

        if args['sex'] is not None:
            qry = qry.filter_by(sex=args['sex'])

        if args['orderby'] is not None:
            if args['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.age))
                else :
                    qry = qry.order_by(Users.age)
            elif args ['orderby'] == 'sex':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.sex))
                else :
                    qry = qry.order_by(Users.sex)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_field))

        return rows, 200

# Routes

api.add_resource(UserList, '', '/')
api.add_resource(UserResource, '', '/<id>')