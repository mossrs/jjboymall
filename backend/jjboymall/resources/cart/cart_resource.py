import json
import time
from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.models.goods import SkuStock
from comment.utils.data_format import *
from comment.utils.decorators import login_required
from comment.utils.connect_redis import redis_cart
from flask import current_app


class Shopping_Cart(Resource):
    """
        购物车
    """
    method_decorators = {
        'delete': [login_required],
        'post': [login_required]
    }

    # 查询购物车
    def get(self):
        return self.set_Shopping_cart('get')

    # 从购物车删除
    def delete(self):
        rp = RequestParser()
        rp.add_argument('sku_list', required=True)
        args = rp.parse_args()
        sku_list_json = args.sku_list
        sku_list = json.loads(sku_list_json)
        return self.set_Shopping_cart('delete', sku_list=sku_list)

    # 添加到购物车
    def post(self):
        rp = RequestParser()
        rp.add_argument('skuNo', required=True)
        rp.add_argument('amount', required=True)
        rp.add_argument('salePrice', required=True)
        rp.add_argument('specialPrice', required=True)
        rp.add_argument('categoryId', required=True)
        args = rp.parse_args()
        sku_no = args.skuNo
        amount = args.amount
        categoryId = args.categoryId
        add_time = int(time.time() * 1000)
        special_price = float(args.specialPrice)
        res_sku = SkuStock.query.filter(SkuStock.sku_no == sku_no)
        if res_sku:
            res_sku = res_sku.with_entities(SkuStock.id, SkuStock.sku_no, SkuStock.price, SkuStock.image, SkuStock.title,
                                            SkuStock.spec, SkuStock.rel_product_id).first()
            cart_data = data_to_dict(res_sku)
            cart_data['categoryId'] = categoryId
            cart_data['specialPrice'] = special_price
            cart_data['amount'] = amount
            cart_data['addTime'] = add_time
            return self.set_Shopping_cart('post', sku_list=[cart_data])
        else:
            return {'message': 'None'}

    # 操作购物车
    @staticmethod
    def set_Shopping_cart(method, sku_list=None):
        user_id = ''
        if sku_list is None:
            sku_list = []
        try:
            user_id = g.user_id
        except Exception as e:
            current_app.logger.info(e)

        cart_cache_json = redis_cart.get(f'cart_from_user_{user_id}')   # 查询缓存
        cart_cache_dict = {}
        if cart_cache_json:                                                     # 当前用户是否有购物车缓存数据
            cart_cache_dict = json.loads(cart_cache_json)
        # 查询
        if method == 'get':
            goods_list = []
            if cart_cache_json:
                for value in cart_cache_dict.values():                          # 提取数据存入列表
                    goods_list.append(value)
            return goods_list

        # 添加到购物车
        if method == 'post':
            add_sku_item = sku_list[0]                                          # 添加到购物车都是单条记录添加
            add_sku_skuNo = add_sku_item.get('sku_no')                          # 要添加到购物车商品的sku码
            if cart_cache_json:
                cache_sku = cart_cache_dict.get(add_sku_skuNo)                  # 查询是否有此商品的缓存
                if bool(cache_sku):
                    cache_sku['amount'] = int(cache_sku['amount']) + int(add_sku_item['amount'])    # 更改数量
                    cache_sku['addTime'] = add_sku_item['amount']                                   # 更改数量
                else:
                    cart_cache_dict[add_sku_skuNo] = add_sku_item               # 无则添加
            else:
                cart_cache_dict = {add_sku_skuNo: add_sku_item}                 # 生成新待缓存的购物车数据
            redis_cart.setex(f'cart_from_user_{user_id}', 3600 * 48, json.dumps(cart_cache_dict))  # 写入redis
            return add_sku_item

        # 从购物车删除
        if method == 'delete':
            for item in sku_list:
                delete_sku_skuNo = item.get('sku_no')                   # 要从购物车删除商品的sku码
                if cart_cache_json:
                    delete_sku = cart_cache_dict.get(delete_sku_skuNo)  # 查询是否有此商品的缓存
                    if delete_sku:
                        del cart_cache_dict[delete_sku_skuNo]
                else:
                    return {'message': '无记录', 'code': 200}
            redis_cart.setex(f'cart_from_user_{user_id}', 3600 * 48, json.dumps(cart_cache_dict))
            return {'msg': 'OK'}









