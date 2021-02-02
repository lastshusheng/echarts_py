# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:18 下午
# @Email   : lastshusheng@163.com


import json
from functools import wraps
from flask import make_response, Response
from enum import Enum
from decimal import Decimal
import datetime
from echarts_data.error_code import ErrorCode, ErrorCodeHelper


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    return wrapper_fun


def key_to_json(data):
    if data is None or isinstance(data, (bool, int, str)):
        return data
    if isinstance(data, (tuple, frozenset)):
        return str(data)
    raise TypeError


def json_converter(obj):
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, dict):
        return {key_to_json(key): json_converter(obj[key]) for key in obj}
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, Decimal):
        return int(obj)


def ret(data=None, err_code=ErrorCode.Success, msg=""):
    if data is None:
        data = {}
    if not msg:
        result = {'data': data, 'errCode': err_code, 'msg': ErrorCodeHelper.transformErrorMsg(err_code)}
    else:
        result = {'data': data, 'errCode': err_code, 'msg': msg}
    response = Response(
        response=json.dumps(result, default=json_converter, skipkeys=True),
        status=200,
        mimetype='application/json'
    )
    return response


def check_param_all(li: list) -> bool:
    """检查必传参数"""
    return all(map(lambda x: str(x) if x is not None else "", li))


def check_param_any(li: list) -> bool:
    """检查必传参数"""
    return any(map(lambda x: str(x) if x is not None else "", li))


def get_page(pagination) -> dict:
    res = {
        "has_prev": pagination.has_prev,
        "has_next": pagination.has_next,
        "page": pagination.page,
        "total_pages": pagination.pages,
        "records": []
    }
    return res
