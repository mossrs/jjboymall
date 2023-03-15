from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
coupon_bp = Blueprint('coupon', __name__, url_prefix='/coupon')
coupon_api = Api(coupon_bp)
coupon_api.representation('application/json')(output_json)


from jjboymall.resources.coupon.coupon_resource import *
coupon_api.add_resource(Coupon_GoodsCoupon, '/goods_coupon', endpoint='goods_coupon')
coupon_api.add_resource(Coupon_UserCoupon, '/user_coupon', endpoint='user_coupon')