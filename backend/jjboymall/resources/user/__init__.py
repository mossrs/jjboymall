from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
user_bp = Blueprint('user', __name__, url_prefix='/user')
user_api = Api(user_bp)
user_api.representation('application/json')(output_json)
# 在函数视图中使用这种装饰器@api.representation('application/json')


# 在用户模块添加请求钩子（看需求加全局还个别）
# from comment.utils.request_ware import jwt_request_authorization
# user_bp.before_request(jwt_request_authorization)
from jjboymall.resources.user.user_resource import *
user_api.add_resource(UserSMS, '/sms', endpoint='sms')
user_api.add_resource(AuthorizationCodeResource, '/authorization', endpoint='authorization')
user_api.add_resource(UserRegisterResource, '/register', endpoint='register')
user_api.add_resource(UserLoginResource, '/login', endpoint='login')
user_api.add_resource(IsExistPhoneResource, '/isExist', endpoint='isExist')
user_api.add_resource(UserLoginOutResource, '/loginOut', endpoint='loginOut')

