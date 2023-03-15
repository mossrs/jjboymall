from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
index_bp = Blueprint('index', __name__, url_prefix='/index')
index_api = Api(index_bp)
index_api.representation('application/json')(output_json)


from jjboymall.resources.index.index_resource import *
index_api.add_resource(ShoppingCategory, '/category')
index_api.add_resource(ShoppingHomeNewProduct, '/home_new_product')
index_api.add_resource(ShoppingHomeRecommendProduct, '/home_recommend_product')
index_api.add_resource(ShoppingRecommendSubject, '/recommend_subject')
