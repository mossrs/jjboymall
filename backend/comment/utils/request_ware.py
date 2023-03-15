from flask import g, request, current_app
from comment.utils.tokens_pyjwt import verify_token


def jwt_request_authorization():
    """
    自定义一个请求钩子函数，验证token，并且把验证成功之后的用户ID保存到全局变量g中
    在flask框架中 因为我用的是json格式（主流一般都是json） 所以只要返回一定是字典（会自动通过out_json变成json数据返回到页面）
    但要注意json不能格式化时间 decimal类型的数据 所以可以通过data_format函数把它变成字符串然后返回
    如果某个方法没有返回值 那就默认返回None
    这个返回要根据业务逻辑灵活去用
    """
    token = request.headers.get('token')
    if token:
        result = verify_token(token)
        if result:
            g.user_id = result['id']


def loggerHook(resp):
    current_app.logger.info(resp)
    return resp




