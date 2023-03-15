import json
from flask_restful import Resource
from comment.models.index import *
from comment.utils.data_format import data_to_dict, datas_to_dict
from comment.utils.connect_redis import redis_index


# 商品分类的资源类(当用户查询时，为了避免频繁调用mysql而引入缓存redis数据库)
class ShoppingCategory(Resource):

    def __init__(self):
        self.redis_data = redis_index.get('index_category')

    def get(self):
        if self.redis_data:
            return json.loads(self.redis_data)
        else:
            # 开发环境下的代码 运行环境下要先让页面展示出来（先自己传一个参数） 但是这个不需要传参数在前端 所以我们就直接指定 parent_id
            data = self.getDate(0)
            if data:
                for item in data:
                    # 这个是在一级分类添加一个键值对用来存放二级分类得到的结果
                    # 根据id来查询（因为我们在创建表示已经吧每个商品的id和对应的级别给添加完了）
                    data_second = self.getDate(item['id'])
                    item['list'] = data_second
                    for items in data_second:
                        data_third = self.getDate(items['id'])
                        items['list'] = data_third
                # 把查询到的数据写到redis 三个参数
                # 1 你指定的键 2 有效时间 3 存数据的值（如果key存在，则会替换旧的值）
                redis_index.setex('index_category', 3600, json.dumps(data))
                return data
            return {'message': 'None'}

    # 该静态方法是查询商品
    @staticmethod
    def getDate(parent_id):
        # 这个with_entities是指定返回的字段（因为我们用这个query只能查全部，不能单独的返回我们想要的，所以加上那个）
        res = Category.query.with_entities(Category.id, Category.parent_id, Category.name) \
            .filter(Category.parent_id == parent_id).order_by(Category.sort.asc()).all()
        if res:
            return datas_to_dict(res)


# 首页新品推荐资源类
class ShoppingHomeNewProduct(Resource):

    def __init__(self):
        self.redis_data = redis_index.get('index_HomeNewProduct')

    def get(self):
        if self.redis_data:
            return json.loads(self.redis_data)
        else:
            res = HomeNewProduct.query.join(Product, HomeNewProduct.product_id == Product.id) \
                .with_entities(Product.id, Product.default_pic, Product.price, Product.product_name,
                               Product.rel_category3_id) \
                .order_by(HomeNewProduct.sort.asc()).limit(10).all()
            if res:
                data = datas_to_dict(res)
                redis_index.setex("index_HomeNewProduct", 3600, json.dumps(data))
                return data
        return {'message': 'None'}


# 首页人气热搜资源类
class ShoppingHomeRecommendProduct(Resource):

    def __init__(self):
        self.redis_data = redis_index.get('index_HomeRecommendProduct')

    def get(self):
        if self.redis_data:
            return json.loads(self.redis_data)
        else:
            res = HomeRecommendProduct.query.join(Product, HomeRecommendProduct.product_id == Product.id) \
                .with_entities(Product.id, Product.default_pic, Product.price, Product.product_name,
                               Product.rel_category3_id) \
                .limit(10).all()
            if res:
                data = datas_to_dict(res)
                redis_index.setex('index_HomeRecommendProduct', 3600, json.dumps(data))
                return data
        return {'message': 'None'}


# 首页专题的资源类
class ShoppingRecommendSubject(Resource):

    def __init__(self):
        self.redis_data = redis_index.get('index_RecommendSubject')

    def get(self):
        if self.redis_data:
            return json.loads(self.redis_data)
        else:
            res = CmsSubject.query.filter(CmsSubject.show_status == 1).all()
            if res:
                data_list = []
                for res_obj in res:
                    data = data_to_dict(res_obj)
                    res_product = CmsSubjectProductRelation.query.join \
                        (Product, CmsSubjectProductRelation.product_id == Product.id).filter \
                        (CmsSubjectProductRelation.subject_id == res_obj.id).with_entities \
                        (Product.id, Product.default_pic, Product.price, Product.product_name,
                         Product.rel_category3_id).limit(10).all()
                    if res_product:
                        data_product = datas_to_dict(res_product)
                        data['productList'] = data_product
                        data_list.append(data)
                redis_index.setex('index_RecommendSubject', 3600, json.dumps(data_list))
                return data_list
        return {'message': 'None'}
