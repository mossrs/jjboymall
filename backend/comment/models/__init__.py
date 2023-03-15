from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# 这个是为了先让我要创建的模型加载到某个模块 然后通过init-->migrate-->upgrade来讲表创建出来
from comment.models.index import *
from comment.models.user import User
from comment.models.goods import *
from comment.models.coupon import *
from comment.models.order import *
from comment.models.address import *


"""
    可参考django的部分类的参数 class Meta的 来变成抽象类 并继承  __abstract_

    优化后的flask-sqlalchemy 我们一般都是用query.filter 且自动关闭 不需要手动关闭   
    除了查询以外 其他都要提交
    查：
        query.filter  不写.first() 或 .all() 返回的是sql语句 类型是<class 'flask_sqlalchemy.BaseQuery'> 
        加上first()或all() 返回的是一行或多行模型类对象（里面包含了模型的一行全部字段） 
        要想实现查询指定字段 可以使用.with_entities(要查询的字段) 查询指定字段 返回AbstractKeyedTuple对象（形似元组 但不是）
        all 都返回列表 只不过列表里可能是模型类对象（db.Model对象） 或 AbstractKeyedTuple（使用with_entities查询）
        first 返回一个 模型类对象（db.Model对象） 或 AbstractKeyedTuple（使用with_entities查询）
        with_entities 返回（一行所有字段的值）AbstractKeyedTuple
    删：
        flask_sqlalchemy只提供了删一行数据 或查出多行遍历删除 db.session.delete(查出来的一行数据) 或query.filter.delete() 
        要想删指定字段 就改把查出来的对象给设为None 
        遍历删除 因为你查出的是列表 直接db.session.delete(列表) 是不行的因为没有映射 只能遍历删把查到的列表一个个放进去delete(1条, 2条 ...)
        且query.（filter()）delete() 切记：不能在delete前加first() 或 all() 因为加了就相当于是个对象 没那个属性
    改：
        查出来直接点语法就行（但只能修改一个） 
        或query.filter(可加过滤条件或不加跟删一样).update({'必须是表的真实字段名': 新的数据}) 相当于重写但不能改变字段名 可重写一个或多个
        要修改字段名的话 我们一般直接把模型修改然后迁移映射 但一般用的很少 在创建表时 我们就已经想好了业务逻辑 
        如果真的需要重新映射 就需要用到migrate来迁移更新 migrate -> upgrade 
        因为你想要将已经映射过的表重新映射 只需要使用migrate在把修改后的表迁移下 然后更新upgrade即可 init一般只在第一次创建时使用 就用一次 
    增：
        相当于实例模型 然后db.session.add(一个实例)  add_all(实例一, 实例二, 实例三 ...])
        
    分页操作 .paginate()
    # 这个分页器 就是里面传两个参数 一个是当前页码（page） 一个是每页数据量（per_page）
            返回一个Pagination的对象 属性如下
            has_next      是否还有下一页
            has_prev      是否还有上一页
            items         当前页的元素集合（数据内容，因为json返回所以需格式化） 返回的是列表
            prev_num      上一页的页码
            next_num      下一页的页码
            page          当前页的页码
            pages         匹配的元素在当前配置一共有多少页
            per_page      每一页显示的元素个数
            query         创建Pagination对象对应的query对象即查询语句
            total         匹配的元素总数
            error_out     默认为True 当没传参数时报错 False则不报错 当没传参数时默认page=1 per_page=20
            
    连接操作 .join()
            里面可以连接多个模型 如模型.query.join(模型一, 模型一与模型的等价关系（on .. 和 ..）, 模型二, 模型二与模型的等价关系, ...)
            .filter(根据业务逻辑啊过滤看需求加前加后)
            
"""


