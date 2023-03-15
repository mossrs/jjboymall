from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# 创建限流器
# 限制器就是为了限制验证的次数
# key_func 是判断函数 表示以何种条件判断算一次访问 因为传的是函数，所以不要调用
# get_remote_address 我们以客户端访问的地址来作为判断依据
limiter = Limiter(key_func=get_remote_address)
