import configparser, json
from datetime import timedelta
from functools import wraps

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Config():
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    # JWT_SECRET_KEY = cfg['jwt']['secret_key']
    HOST_MATAUANG = cfg['matauang']['host1']
    KEY_MATAUANG = cfg['matauang']['key1']
    X_HOST = cfg['amazon']['host2']
    X_APIKEY = cfg['amazon']['key2']
    EMAIL_KEY = cfg['email']['api_key']
    EMAIL_SECRET = cfg['email']['api_secret']
    WEATHER_KEY = cfg['weather']['api_key']
    
    
class DevelopmentConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
    APP_PORT = 9090

class ProductionConfig(Config):
    APP_DEBUG = False
    DEBUG = False
    MAX_BYTES = 10000
    APP_PORT = 5050