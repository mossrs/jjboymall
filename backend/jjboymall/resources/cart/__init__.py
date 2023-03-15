from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_api = Api(cart_bp)
cart_api.representation('application/json')(output_json)


from jjboymall.resources.cart.cart_resource import *
cart_api.add_resource(Shopping_Cart, '/user_cart', endpoint='user_cart')


