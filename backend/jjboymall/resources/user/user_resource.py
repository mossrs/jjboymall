import random
import json
from flask import current_app, request
from flask_restful.reqparse import RequestParser
from flask_restful import Resource
from flask_limiter.util import get_remote_address
from comment.utils.limitr import limiter as lmt
from comment.utils.connect_redis import redis_user
from comment.utils import aliyun_sms_send, huyi_sms
from comment.utils.parser import mobile_parser, regex, email_parser
from comment.utils.tokens_pyjwt import generate_token
from comment.utils.decorators import login_required
from comment.models.user import User
from comment.models import db


class UserSMS(Resource):
    """
        客户通过输入手机号来得到验证码（因为如果手机号为假就收不到，所以不用在这里验证）
        但现在我们没有短信没法注册 所以就先学 等后面有了在学
        这个是加了限流器的发送短信类
    """

    decorators = [
        # 添加限流器来限制发送短信次数（可添加多个） （限流种类（时间， IP等）， 目标函数， 提示信息）
        lmt.limit('1/minute',
                  key_func=lambda: request.args['phone'],
                  error_message='Too many requests.'),
        lmt.limit('10/hour',
                  key_func=get_remote_address,
                  error_message='Too many requests.')
    ]

    def __init__(self):
        self.phone = request.form.get('phone').strip()
        self.code = random.randint(100000, 999999)

    def post(self):
        # 通过阿里云平台的发短信功能来发送短信（一个手机号， 一个验证码）返回一个json字符串
        # result = aliyun_sms_send.send_sms(self.phone, str(self.code))
        # # 使用loads吧json变成字典
        # result = json.loads(result)
        # result['phone'] = self.phone
        # 这个redis数据库的setex里面三个参数：键 时效 值
        # 通过这个方法来将短信验证码存放到redis中
        # redis_user.setex(f'shopping:code{self.phone}', 300, self.code)
        # return result

        # 通过互亿无线平台
        result = huyi_sms.send_sms_code(str(self.code), self.phone)
        result = json.loads(result)
        redis_user.setex('sms_%s' % self.phone, 60, self.code)
        return result


class AuthorizationCodeResource(Resource):
    """
        客户如果收到了验证码，这个通过校验验证码来判断是否是本人操作
    """

    def __init__(self):
        rp = RequestParser()
        rp.add_argument('phone', type=mobile_parser, required=True)
        rp.add_argument('code', type=regex(r'^\d{6}$'), required=True)
        args = rp.parse_args()
        self.phone = args.phone
        self.code = args.code

    def post(self):
        # 从redis得到之前保存的验证码
        key = f'sms_{self.phone}'
        try:
            real_code = redis_user.get(key)
        except ConnectionError as e:
            current_app.logger.error(e)
            return {'message': 'redis db connect error'}, 400
        if not real_code or real_code.decode() != self.code:
            return {'message': 'Invalid code'}, 400
        return {'phone': self.phone, 'msg': 'Code is right'}


class UserRegisterResource(Resource):
    """
        填写账号信息 完成用户注册
    """

    def __init__(self):
        rp = RequestParser()
        rp.add_argument('username', required=True)
        rp.add_argument('password', required=True)
        rp.add_argument('phone', type=mobile_parser, required=True)
        rp.add_argument('email', type=email_parser, required=True)
        args = rp.parse_args()
        self.username = args.username
        self.password = args.password
        self.phone = args.phone
        self.email = args.email

    def post(self):
        u = User.query.filter(User.username == self.username).first()
        if u:
            current_app.logger.info(f'{self.username}:用户已经存在，请重新输入')
            return {'message': 'The username already exists'}, 400

        # 把用户信息保存到数据库中
        # 这个地方要用pwd=因为前面我使用装饰器将pwd变成User的属性了（但pycharm的提示没有检测到）
        # 注意我们现在因为没有短信验证服务，所以现在就在postman上注册登录必须有下面四个表单元素
        # 正常来说 如果有短信服务的话 前端会在注册时只显示用户名 密码 邮箱没有手机号（因为已经短信验证过了）
        # 所以有短信验证时 我们后端的代码需要吧映射模型的手机号给去掉
        u = User(username=self.username, pwd=self.password, phone=self.phone, email=self.email, status=0)
        db.session.add(u)
        db.session.commit()
        return {'msg': 'OK'}


class UserLoginResource(Resource):
    """
        登录
    """

    def __init__(self):
        self.username = request.form.get('username')
        self.password = request.form.get('password')

    def post(self):
        if not all([self.username, self.password]):
            return {'message': 'Empty Params'}, 400
        user = User.query.filter(User.username == self.username).first()
        if user:
            if user.check_passwd(self.password):
                token = generate_token(user.id)
                return {'msg': 'Login Successfully', 'token': token, 'username': self.username}
        return {'message': 'Login Failed'}


class UserLoginOutResource(Resource):
    """
        退出登录
    """

    method_decorators = {
        'post': [login_required]
    }

    def post(self):
        return {'msg': 'LoginOut Successfully'}


class IsExistPhoneResource(Resource):
    """
    判断手机号是否存在 注册时
    """

    def __init__(self):
        self.phone = request.form.get('phone')

    def post(self):
        user = User.query.filter(User.phone == self.phone).first()
        if user:
            return {'IsExist': True, 'message': "It's existed", 'code': 201}
        return {'msg': 'You can Register'}
