# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:17 下午
# @Email   : lastshusheng@163.com


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager


db = SQLAlchemy()
migrate = Migrate()
manager = Manager()


@manager.command
def initdb():
    db.create_all()
