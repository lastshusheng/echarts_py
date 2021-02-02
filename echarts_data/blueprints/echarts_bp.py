# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:05 下午
# @Email   : lastshusheng@163.com


import random
import datetime
from flask import Blueprint, request
from echarts_data.extensions import db
from echarts_data.utils import ret, check_param_all
from echarts_data.error_code import ErrorCode
from echarts_data.models.echarts_mod import Table1, Table2

echarts_bp = Blueprint('echarts_bp', __name__)


@echarts_bp.route('/get_random_data', methods=['GET'])
def get_random_data():
    """
    获取随机数据
    :return:
    """
    # 生成x轴和y轴数据
    x_axis = [str(i) for i in range(50)]  # x轴也可以是动态的
    y_axis = [random.randint(10, 100) for i in range(50)]
    data = {
        'xAxis': x_axis,
        'yAxis': y_axis
    }
    x_y_map = dict(zip(x_axis, y_axis))
    obj_table1 = Table1.query.filter(Table1.title.in_(x_axis)).all()
    # 如果x轴是动态的就需要判断数据库中是否有，有的话就更新
    for table1 in obj_table1:
        if table1.title in x_axis:
            table1.value = x_y_map.pop(table1.title)
            db.session.add(table1)
    sub_data = []
    # 将不在数据库中的数据插入数据库
    for k, v in x_y_map.items():
        sub_data.append({'title': k, 'value': v})
    if sub_data:
        db.session.execute(
            Table1.__table__.insert(),
            sub_data
        )
    db.session.commit()
    res = {
        'data': data
    }
    return ret(res)


@echarts_bp.route('/save_data', methods=['POST'])
def save_data():
    """
    存储数据
    :return:
    """
    x_axis = request.json.get('xAxis')
    y_axis = request.json.get('yAxis')
    if not x_axis or not y_axis:
        return ret(err_code=ErrorCode.ParamsError)
    if len(x_axis) != len(y_axis):
        return ret(err_code=ErrorCode.ParamsError)

    db.session.execute(
        Table2.__table__.insert(),
        [{'title': x, 'value': y_axis[i]} for i, x in enumerate(x_axis)]
    )
    db.session.commit()
    return ret()


@echarts_bp.route('/get_saved_data', methods=['GET'])
def get_saved_data():
    """
    获取存储的数据
    :return:
    """
    obj_table2 = Table2.query.order_by(Table2.id.desc()).limit(100)
    x_axis = []
    y_axis = []
    for table2 in obj_table2:
        x_axis.append(table2.title)
        y_axis.append(table2.value)
    x_axis.reverse()
    y_axis.reverse()
    data = {
        'xAxis': x_axis,
        'yAxis': y_axis
    }
    res = {
        'data': data
    }
    return ret(res)

