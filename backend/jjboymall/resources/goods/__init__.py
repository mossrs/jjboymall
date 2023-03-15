from flask import Blueprint
from flask_restful import Api
from comment.utils.out_json import output_json
goods_bp = Blueprint('goods', __name__, url_prefix='/goods')
goods_api = Api(goods_bp)
goods_api.representation('application/json')(output_json)


from jjboymall.resources.goods.goods_resource import *
goods_api.add_resource(Goods_GoodsList, '/goods_list')
goods_api.add_resource(Goods_GoodsSpecification, '/goods_specification')
goods_api.add_resource(Goods_GoodsDetail, '/good_detail')
goods_api.add_resource(Goods_GoodsFullReduction, '/good_fullReduction')
goods_api.add_resource(Goods_MerchantHotsales, '/merchant_hotsales')
goods_api.add_resource(Goods_GoodSkuDetail, '/good_sku_detail')
goods_api.add_resource(Goods_CartSkuDetail, '/goods_cart_sku_detail', endpoint='goods_cart_sku_detail')
goods_api.add_resource(Goods_Recommend, '/goods_cart_recommend')
