# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:16 下午
# @Email   : lastshusheng@163.com


import os
import datetime

BASE_DIR = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
APP_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'develop'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:wss996124@127.0.0.1:3306/echarts?charset=utf8mb4'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    REDIS_URL = 'redis://:@localhost:6379/0'


class TestingConfig(BaseConfig):
    # TODO 待补充
    pass


class ProductionConfig(BaseConfig):
    # TODO 待补充
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
