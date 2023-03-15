from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
address_bp = Blueprint('address', __name__, url_prefix='/address')
address_api = Api(address_bp)
address_api.representation('application/json')(output_json)


from jjboymall.resources.address.address_resource import *
address_api.add_resource(User_Address, '/user_address')


