# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:04 下午
# @Email   : lastshusheng@163.com

from echarts_data.extensions import db
from datetime import datetime
from .base_mod import DataMixin


class Table1(db.Model, DataMixin):
    """
    表1
    """
    __tablename__ = 'tb_table1'

    title = db.Column(db.String(32))
    value = db.Column(db.Integer, default=0, server_default='0')  # 这里根据值的类型设置是否使用DECIMAL类型


class Table2(db.Model, DataMixin):
    """
    表2
    """
    __tablename__ = 'tb_table2'

    title = db.Column(db.String(32))
    value = db.Column(db.Integer, default=0, server_default='0')  # 这里根据值的类型设置是否使用DECIMAL类型
