import json, logging, config, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from functools import wraps

from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

app = Flask(__name__)
jwt = JWTManager(app)


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == 'false' or claims['status'] == 'False':
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if os.environ.get('FLASK_ENV', 'Production') == "Production":
    app.config.from_object(config.ProductionConfig)
elif os.environ.get('FLASK_ENV', 'Production') == "Testing":
    app.config.from_object(config.Testing)
else:
    app.config.from_object(config.DevelopmentConfig)
    

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
        app.logger.error("REQUEST_LOG\t%s",
            json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            }))
    
    return response

from blueprints.client.resources import bp_client
app.register_blueprint(bp_client, url_prefix='/client')

from blueprints.user.resources import bp_user
app.register_blueprint(bp_user, url_prefix='/user')

from blueprints.auth import bp_auth
app.register_blueprint(bp_auth, url_prefix='/auth')

from blueprints.conversion.resources import bp_conversion
app.register_blueprint(bp_conversion, url_prefix='/conversion')

from blueprints.amazon.resources import bp_amazon
app.register_blueprint(bp_amazon, url_prefix='/amazon')

from blueprints.email.resources import bp_email
app.register_blueprint(bp_email, url_prefix='/email')

from blueprints.weather.resources import bp_weather
app.register_blueprint(bp_weather, url_prefix='/weather')

db.create_all()