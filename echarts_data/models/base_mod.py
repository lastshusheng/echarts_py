# @Author  : Shusheng Wang
# @Time    : 2021/2/2 8:03 下午
# @Email   : lastshusheng@163.com


from echarts_data.extensions import db
from datetime import datetime


class DataMixin(object):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)

    def to_dict(self, need_id=False):
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        _dict = {}
        for col in self.__table__.columns:
            if isinstance(col.type, db.DateTime):
                value = convert_datetime(getattr(self, col.name))
            elif isinstance(col.type, db.Numeric):
                value = float(getattr(self, col.name))
            else:
                value = getattr(self, col.name)
            _dict[col.name] = value

        # 相关属性不能暴露出去
        if not need_id:
            _dict.pop('id')
        return _dict

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def del_to_db(self):
        db.session.delete(self)
        db.session.commit()
