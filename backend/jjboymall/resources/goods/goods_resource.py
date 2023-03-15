import json
from flask_restful import Resource, reqparse
from flask import request
from comment.models.goods import *
from comment.models.index import *
from comment.utils.data_format import *


class Goods_GoodsList(Resource):
    """
        商品列表
    """

    def __init__(self):
        rq = reqparse.RequestParser()
        rq.add_argument('page', required=True, type=int)  # page
        rq.add_argument('size', required=True, type=int)  # per_page
        req = rq.parse_args()
        self.page = req.page
        self.size = req.size
        self.relCategory1Id = request.form.get('relCategory1Id')
        self.relCategory2Id = request.form.get('relCategory2Id')
        self.relCategory3Id = request.form.get('relCategory3Id')
        self.search_word = request.form.get('productName')

    def select_search(self):
        res_filter = None
        if self.relCategory1Id:
            res_filter = Product.query.filter(Product.rel_category1_id == self.relCategory1Id)
        elif self.relCategory2Id:
            res_filter = Product.query.filter(Product.rel_category2_id == self.relCategory2Id)
        elif self.relCategory3Id:
            res_filter = Product.query.filter(Product.rel_category3_id == self.relCategory3Id)
        elif self.search_word:
            res_filter = Product.query.filter(Product.product_name.like("%" + self.search_word + "%"))
        if res_filter:
            res = res_filter.with_entities(Product.id, Product.default_pic, Product.price, Product.product_name,
                                           Product.rel_category3_id).paginate(self.page, per_page=self.size,
                                                                              error_out=False)
            return res
        return None

    def post(self):
        res = self.select_search()
        if res.items:
            data = {'has_next': res.has_next, 'has_prev': res.has_prev, 'next_num': res.next_num, 'page': res.page,
                    'pages': res.pages, 'total': res.total, 'content': datas_to_dict(res.items)}
            return data
        return {'message': 'None', 'code': 200}


class Goods_GoodsSpecification(Resource):
    """
        商品规格
    """

    def __init__(self):
        self.relCategory1Id = request.form.get('relCategory1Id')
        self.relCategory2Id = request.form.get('relCategory2Id')
        self.relCategory3Id = request.form.get('relCategory3Id')
        self.search_word = request.form.get('productName')

    def get_spec_list(self):
        res_filter = None
        if self.relCategory1Id:
            res_filter = Product.query.filter(Product.rel_category1_id == self.relCategory1Id)
        elif self.relCategory2Id:
            res_filter = Product.query.filter(Product.rel_category2_id == self.relCategory2Id)
        elif self.relCategory3Id:
            res_filter = Product.query.filter(Product.rel_category3_id == self.relCategory3Id)
        elif self.search_word:
            res_filter = Product.query.filter(Product.product_name.like("%" + self.search_word + "%"))
        if res_filter:
            spec = res_filter.with_entities(Product.spec_options).first()
            if spec:
                product_spec = spec.spec_options.split(',')
                spec_list = []
                for spec in product_spec:
                    # 用规格id查询规格的名称和id （颜色 内存 屏幕大小等）
                    spec_all = Specification.query.filter(Specification.id == int(spec)) \
                        .with_entities(Specification.name, Specification.id).first()
                    # 用规格id查询规格的具体分类 （ 颜色下面的，红色，蓝色等）
                    spec_info = SpecificationOption.query.filter(SpecificationOption.rel_spec_id == int(spec)) \
                        .with_entities(SpecificationOption.name, SpecificationOption.id, SpecificationOption.enabled,
                                       SpecificationOption.rel_spec_id).all()
                    optionList = datas_to_dict(spec_info)
                    spec_list.append(
                        {
                            'specId': spec_all.id,
                            'specName': spec_all.name,
                            'optionList': optionList
                        }
                    )
                return spec_list
        return None

    def post(self):
        res = self.get_spec_list()
        return res or {'message': 'None', 'code': 200}


class Goods_GoodsDetail(Resource):
    """
        商品详情
    """

    def __init__(self):
        rq = reqparse.RequestParser()
        rq.add_argument('good_id', type=int)
        req = rq.parse_args()
        self.product_id = req.good_id

    def get(self):
        product_res = Product.query.filter(Product.id == self.product_id).first()
        if product_res:
            goods_detail_data = data_to_dict(product_res)
            pro_sku_data = self.get_sku_data(self.product_id)
            goods_detail_data['skuList'] = [pro_sku_data]
            spec_list = []
            spec_all = Specification.query.filter(Specification.rel_category_id == product_res.rel_category3_id) \
                .with_entities(Specification.id, Specification.name, Specification.rel_category_id,
                               Specification.rel_spec_type_id).all()
            for spec in spec_all:
                temp_data = data_to_dict(spec)
                spec_info = SpecificationOption.query.filter(SpecificationOption.rel_spec_id == spec.id) \
                    .with_entities(SpecificationOption.name, SpecificationOption.id, SpecificationOption.enabled,
                                   SpecificationOption.rel_spec_id).all()
                option_list = datas_to_dict(spec_info)
                temp_data['optionDTOS'] = option_list
                spec_list.append(temp_data)
            goods_detail_data['specList'] = spec_list
            return goods_detail_data
        return {'message': 'None', 'code': 200}

    @staticmethod
    def get_sku_data(product_id):
        # 获取查询的产品的sku
        pro_sku_res = SkuStock.query.filter(SkuStock.rel_product_id == product_id).first()
        pro_sku_data = data_to_dict(pro_sku_res)
        # 获取sku下面的规格列表
        specTypeList = json.loads(pro_sku_data['spec'])
        pro_sku_data['specTypeList'] = specTypeList
        return pro_sku_data


class Goods_GoodsFullReduction(Resource):
    """
        商品满减
    """

    def __init__(self):
        rq = reqparse.RequestParser()
        rq.add_argument('good_id', type=int)
        req = rq.parse_args()
        self.product_id = req.good_id

    @staticmethod
    def get_fullReduction(product_id):
        res = ProductFullReduction.query.filter(ProductFullReduction.product_id == product_id).with_entities(
            ProductFullReduction.id, ProductFullReduction.product_id, ProductFullReduction.full_price,
            ProductFullReduction.reduce_price, ProductFullReduction.start_time, ProductFullReduction.end_time).all()
        data_list = []
        if res:
            for item in res:
                res_data = data_to_dict(item)
                data_list.append(res_data)
            return data_list
        else:
            return {'message': 'None', 'code': 200}

    def get(self):
        return self.get_fullReduction(self.product_id)


class Goods_MerchantHotsales(Resource):
    """
    商家热卖
    """

    def __init__(self):
        rq = reqparse.RequestParser()
        rq.add_argument('merchant_id', type=int)
        req = rq.parse_args()
        self.merchant_id = req.merchant_id

    def get(self):
        res = Product.query.filter(Product.rel_tenant_id == self.merchant_id).order_by(-Product.sales_num).limit(
            5).all()
        if res:
            return datas_to_dict(res)
        return {'msg': 'None'}


class Goods_Recommend(Resource):
    """
    商品推荐 (购物车)
    """

    def __init__(self):
        rq = reqparse.RequestParser()
        rq.add_argument('relProductId', type=int)
        req = rq.parse_args()
        self.rel_productId = req.relProductId

    def post(self):
        res = Product.query.filter(Product.rel_category3_id == self.rel_productId).order_by(-Product.sales_num).limit(
            8).all()
        if res:
            return datas_to_dict(res)
        return {'message': 'None', 'code': 200}


class Goods_GoodSkuDetail(Resource):
    """
    获取产品sku 如果库存为0我们也要让他展示页面，只不过是没数据罢了 要根据需求灵活
    """

    def __init__(self):
        rq = reqparse.RequestParser()
        rq.add_argument('productId', type=int)
        rq.add_argument('optionIds', type=str)
        req = rq.parse_args()
        self.productId = req.productId
        self.optionIds = req.optionIds

    def post(self):
        res_sku = SkuStock.query.filter(SkuStock.rel_product_id == self.productId,
                                        SkuStock.option_ids == self.optionIds).first()
        if res_sku:
            sku_data = data_to_dict(res_sku)
            specTypeList = json.loads(sku_data['spec'])
            sku_data['specTypeList'] = specTypeList
            return sku_data
        else:
            return {'message': 'None'}, 200


class Goods_CartSkuDetail(Resource):
    """
    购物车 优惠sku
    """

    @staticmethod
    def get_sku_by_id(sku_id):
        res_sku = SkuStock.query.filter(SkuStock.id == sku_id).with_entities(SkuStock.id, SkuStock.price).first()
        if res_sku:
            return data_to_dict(res_sku)
        else:
            return {'message': 'None'}

    def post(self):
        rq = reqparse.RequestParser()
        rq.add_argument('sku_list', required=True)
        req = rq.parse_args()
        sku_list = req.sku_list
        sku_list_json = json.loads(sku_list)  # 购物车的sku列表
        data_list = []
        for item in sku_list_json:
            sku_id = item['skuId']
            num = int(item['num'])
            product_id = SkuStock.query.filter(SkuStock.id == sku_id).first().rel_product_id
            # sku对应商品的满减
            res = ProductFullReduction.query.filter(ProductFullReduction.product_id == product_id) \
                .with_entities(ProductFullReduction.id, ProductFullReduction.reduce_price,
                               ProductFullReduction.full_price).first()
            if res:
                item_full_reduction = data_to_dict(res)
                # sku信息，sku价格 sku id
                item_sku_info = self.get_sku_by_id(sku_id)
                reduce_price = item_full_reduction['reduce_price']
                if item_sku_info['price'] * num >= item_full_reduction['full_price']:
                    discountPrice = item_sku_info['price'] * num - reduce_price
                else:
                    discountPrice = item_sku_info['price'] * num
                    reduce_price = 0
                data = {
                    'discountPrice': discountPrice,
                    'originPrice': item_sku_info['price'],
                    'reducePrice': reduce_price,
                    'reductionId': item_full_reduction['id'],
                    'skuId': item_sku_info['id']
                }
                data_list.append(data)
        return data_list
