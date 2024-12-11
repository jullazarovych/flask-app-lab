
class Config:
    SECRET_KEY = "secret-tsh"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_data.sqlite'
    TESTING = True
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_data.sqlite'
    DEBUG = False

config = {
    'default': Config,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
