import jwt
from datetime import datetime, timedelta
from comment.utils.constants import *
from flask import current_app


def generate_token(uid):
    # 参数一：payload{一部字典，负载即加密是带的一些特定信息（用户信息 过期时间等）}
    # 参数二：密钥
    # 参数三：算法 SHA256 MD5 HS256
    # 这个payload里的exp 就只能写 'exp' 后面跟时间（虽然不支持转json但源码里的解释器会自动把他变成字符串） 其他内容可以是自定义的用户信息
    # 如果不写exp 就需要手动讲那个时间转字符串str() 如 'expire' : str(时间)
    # 且这个时间是世界标准的格林尼治时间 需要使用utcnow() 然后再加上timedelta（这个是你要设置的过期时间 当token产生后以标准时间为起点）
    # 等到了你加上的时间（seconds, minute, hour, day, year, month） token就会失效
    # 所以exp就是（按照标准时间设置的） 因为你使用了timedelta +相当于延长 -相当于提前
    payload = {
        'id': uid,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    s = jwt.encode(payload=payload, key=TOKEN_KEY, algorithm='HS256')
    # 这个s就是加密后的token（字符串类型）注意--->加密是algorithm
    return s


def verify_token(token_str):
    # 本质上就是解密过程 注意--->解密是algorithms 返回你当时在加密时的payload里的数据（字典）
    # 在实际应用中 我们为了不让无效token报错 使用try
    # 且在导入别的包的模块里的常量时 如果那个常量是一个随机数 则在一次运行时 那个随机数不会变
    # 比如 在生成token时使用了随机数 验证时也用了 此时的随机数还是原来的所以才能成功验证token 如果在同一模块使用则会报密钥出错
    try:
        data = jwt.decode(token_str, key=TOKEN_KEY, algorithms='HS256')
        return data
    except Exception as e:
        current_app.logger.info(e)






