from comment.models import db


class SmsCoupon(db.Model):
    __tablename__ = 't_sms_coupon'
    __table_args__ = {'comment': '优惠券表'}

    id = db.Column(db.BIGINT, primary_key=True)
    type = db.Column(db.Integer, comment='优惠卷类型；0->全场赠券；1->会员赠券；2->购物赠券；3->注册赠券')
    name = db.Column(db.String(100), comment='名称')
    platform = db.Column(db.Integer, comment='使用平台：0->全部；1->移动；2->PC')
    count = db.Column(db.Integer, comment='数量')
    amount = db.Column(db.Float(10, 2), nullable=False, comment='金额')
    per_limit = db.Column(db.Integer, comment='每人限领张数')
    min_point = db.Column(db.Float(10, 2), nullable=False, comment='使用门槛；0表示无门槛')
    start_time = db.Column(db.BIGINT, nullable=False, comment='开始使用时间')
    end_time = db.Column(db.BIGINT, nullable=False, comment='结束使用时间')
    use_type = db.Column(db.Integer, nullable=False, comment='使用类型：0->全场通用；1->指定分类；2->指定商品')
    note = db.Column(db.String(200), comment='备注')
    publish_count = db.Column(db.Integer, comment='发行数量')
    use_count = db.Column(db.Integer, comment='已使用数量')
    receive_count = db.Column(db.Integer, comment='领取数量')
    enable_time = db.Column(db.BIGINT, nullable=False, comment='可以领取的日期')
    code = db.Column(db.String(64), comment='优惠码')
    member_level = db.Column(db.Integer, comment='可领取的会员类型：0->无限制')


class SmsCouponHistory(db.Model):
    __tablename__ = 't_sms_coupon_history'
    __table_args__ = {'comment': '优惠券领取历史表'}

    id = db.Column(db.BIGINT, primary_key=True)
    coupon_id = db.Column(db.BIGINT, comment='优惠券id')
    member_id = db.Column(db.String(50), comment='会员id')
    order_id = db.Column(db.String(50), comment='订单id')
    coupon_code = db.Column(db.String(64), comment='优惠券码')
    member_nickname = db.Column(db.String(64), comment='领取人昵称')
    get_type = db.Column(db.Integer, comment='获取类型：0->后台赠送；1->主动获取')
    create_time = db.Column(db.BIGINT, comment='创建时间')
    use_status = db.Column(db.Integer, comment='使用状态：0->未使用；1->已使用；2->已过期')
    use_time = db.Column(db.BIGINT, comment='使用时间')
    order_sn = db.Column(db.String(100), comment='订单号码')


class SmsCouponProductCategoryRelation(db.Model):
    __tablename__ = 't_sms_coupon_product_category_relation'
    __table_args__ = {'comment': '优惠券和商品分类关联表'}

    id = db.Column(db.BIGINT, primary_key=True)
    coupon_id = db.Column(db.BIGINT, comment='优惠券id')
    product_category_id = db.Column(db.BIGINT, comment='商品分类id')
    product_category_name = db.Column(db.String(200), comment='商品分类名称')
    parent_category_name = db.Column(db.String(200), comment='父分类名称')


class SmsCouponProductRelation(db.Model):
    __tablename__ = 't_sms_coupon_product_relation'
    __table_args__ = {'comment': '优惠券和商品关联表'}

    id = db.Column(db.BIGINT, primary_key=True)
    coupon_id = db.Column(db.BIGINT, comment='优惠券id')
    product_id = db.Column(db.BIGINT, comment='商品id')
    product_name = db.Column(db.String(500), comment='商品名称')
    product_sn = db.Column(db.String(200), comment='商品条码')
