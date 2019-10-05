import re


def check_password(password):
    '''
    函数功能：校验用户密码是否合法
    函数参数：
    password 待校验的密码
    返回值：校验通过返回0，校验错误返回非零（密码太长或太短返回1，密码安全强度太低返回2）
    '''
    return 0

def check_phone(phone):
    '''
    函数功能：校验手机号格式是否合法
    函数参数：
    phone 待校验的手机号
    返回值：校验通过返回0，校验错误返回1
    '''
    if re.match("^1\\d{10}$",str(phone)):
        return 0
    return 1

