from itsdangerous import TimedJSONWebSignatureSerializer
from constants import TOKEN_KEY
from flask import current_app
from comment.models.user import User


def generate_token(uid):
    """
    根据已经登陆之后的用户ID，生成token
    :param uid:
    :return: 生成token(因为这个生成token的方法会自动序列化，所以要解码且我们用字典比较好）
    """
    # 参数一：密钥  参数二：token有效时间（会话有效时间）
    # 这个s of type TimedJSONWebSignatureSerializer is not JSON serializable 所以才有下面的写法 （且dumps可以附带信息）
    # 因为这个本身返回的是字节数据类型就算dumps 内容是json的字符串但需要解码后才能变成字符串类型
    s = TimedJSONWebSignatureSerializer(secret_key=TOKEN_KEY, expires_in=3600)
    return s.dumps({'id': uid}).decode()


def verify_token(token_str):
    """
    验证token 成功之后返回用户ID
    :param token_str:
    :return: 返回ID
    """
    s = TimedJSONWebSignatureSerializer(secret_key=TOKEN_KEY)
    try:
        # 本质上就是解密过程
        data = s.loads(token_str)
    except Exception as e:
        current_app.logger.info(e)
        return {'message': 'Token Failed'}
    # 验证成功后，还需要看用户状态是否正常
    user = User.query.filter(User.id == data['id']).first()
    if user and user.status != 0:
        return {'message': 'Status Failed'}
    return {'id': user.id}


