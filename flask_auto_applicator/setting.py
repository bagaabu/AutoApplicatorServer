import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


class Config(dict):
    def __init__(self):
        dict.__init__(self)

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return getattr(self, item)

    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Life is short, you need Python'


class DevelopmentConfig(Config):
    DEBUG = True
    MAX_CONTENT_LENGTH = 20*1024*1024


class TestingConfig(Config):
    DEBUG = True
    MAX_CONTENT_LENGTH = 20*1024*1024


class ProductionConfig(Config):
    MAX_CONTENT_LENGTH = 20*1024*1024


confmap = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

import os

env = os.environ.get('FLASK_ENV', 'production')
env = os.environ.get('FLASK_ENV', 'development')
config = confmap.get(env)()