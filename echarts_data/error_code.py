# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:17 下午
# @Email   : lastshusheng@163.com


from enum import Enum


class ErrorCode(Enum):
    ParamsError = -3
    Success = 0


class ErrorCodeHelper:
    @classmethod
    def transformErrorMsg(cls, errCode):
        msg = ""
        if errCode == ErrorCode.ParamsError:
            msg = "参数错误"
        elif errCode == ErrorCode.Success:
            msg = "成功"
        return msg
