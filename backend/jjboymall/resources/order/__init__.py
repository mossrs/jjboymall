from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
order_bp = Blueprint('order', __name__, url_prefix='/order')
order_api = Api(order_bp)
order_api.representation('application/json')(output_json)


from jjboymall.resources.order.order_resource import *
order_api.add_resource(Shopping_Order, '/shopping_order', endpoint='shopping_order')
order_api.add_resource(Shopping_Order_List, '/shopping_order_list', endpoint='shopping_order_list')


