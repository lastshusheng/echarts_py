# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:17 下午
# @Email   : lastshusheng@163.com


from enum import Enum


class ErrorCode(Enum):
    ParamsError = -3
    Success = 0


class ErrorCodeHelper:
    @classmethod
    def transform_error_msg(cls, err_code):
        msg = ""
        if err_code == ErrorCode.ParamsError:
            msg = "参数错误"
        elif err_code == ErrorCode.Success:
            msg = "成功"
        return msg
