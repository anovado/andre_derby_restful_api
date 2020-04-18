from flask import Flask, request
from flask_restful import Resource, Api
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

app = Flask(__name__)
jwt = JWTManager(app)
# if os.environ.get('FLASK_ENV', 'Production') == "Production":
#     app.config.from_object(config.ProductionConfig)
# else:
#     app.config.from_object(config.DevelopmentConfig)

# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     return{
#         'claims': identity,
#         'identifier': "ATA-BATCH5"
#     }

# def internal_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         verify_jwt_in_request()
#         claims = get_jwt_claims()
#         if not claims['status']:
#             return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
#         else:
#             return fn(*args, **kwargs)
#     return wrapper
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta123@localhost:3306/API'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
manager = Manager(app)
# manager.add_command('db', MigrateCommand)


# from blueprints.book.resources import bp_book

# app.register_blueprint(bp_book, url_prefix='/book')

# add log method
@app.after_request
def after_request(response) :
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
            json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        app.logger.error("")
    
    return response
    # if request.method == 'GET' :
    #     app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request' : request.args.to_dict(), 'response' : json.loads(response.data.decode('utf-8'))}))
    # else :
    #     app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request' : request.get_json(), 'response' : json.loads(response.data.decode('utf-8'))}))

    # return response




from blueprints.conversion.resources import bp_conversion
app.register_blueprint(bp_conversion, url_prefix='/conversion')


# db.create_all()