import re


def mobile_parser(mobile_str):
    """
    检验手机号格式
    :param mobile_str: str 被检验字符串
    :return: mobile_str
    """
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError('{} is not a valid mobile'.format(mobile_str))


def regex(pattern):
    """
    正则校验
    :param pattern: str 正则表达式
    :return: 返回
    """
    def validate(value_str):
        """
        具体校验一个字符串,根据自定义的正则表达式
        :param value_str: 验证的值
        :return:
        """
        if re.match(pattern, value_str):
            return value_str
        else:
            raise ValueError('{} is not a valid params.'.format(value_str))

    return validate


def email_parser(email_str):
    """
        检验邮箱地址格式
        :param email_str: str 被检验字符串
        :return: email_str
        """
    # 注意  | 左右两边加空格的话也会匹配 （虽然习惯加空格为了好看 但此时要注意）
    if re.match('^\w+((-\w+)|(\.\w+))*@[A-Za-z0-9]+((\.)|(-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$', email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))

