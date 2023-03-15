from comment.models import db


class Order(db.Model):
    __tablename__ = 't_order'
    __table_args__ = {'comment': '订单表'}

    id = db.Column(db.BIGINT, primary_key=True, comment='主键')
    user_id = db.Column(db.String(50), nullable=False, comment='用户id')
    order_number = db.Column(db.String(64), nullable=False, index=True, comment='订单编号')
    parent_order_number = db.Column(db.String(64),  comment='父订单编号')
    gmt_create = db.Column(db.BIGINT, nullable=False, comment='提交时间')
    title = db.Column(db.String(255), nullable=False, default='订单标题', comment='订单标题')
    merchant_id = db.Column(db.String(64),  comment='商家编号')
    total_amount = db.Column(db.Float(10, 2), nullable=False, comment='订单金额')
    pay_amount = db.Column(db.Float(10, 2), nullable=False, comment='实际支付金额')
    pay_type = db.Column(db.Integer, nullable=False, comment='支付方式：0->未支付；1->支付宝；2->微信')
    source_type = db.Column(db.Integer, default=0, nullable=False, comment='订单来源：0->PC订单；1->app订单')
    order_status = db.Column(db.Integer, default=0, nullable=False, comment='订单状态：0->待付款；1->待发货；2->待收货；3->交易完成；4'
                                                                            '->已取消；5->超时取消:6->无效订单')
    order_type = db.Column(db.Integer, nullable=False, default=0, comment='订单类型：0->正常订单；1->秒杀订单')
    auto_confirm_day = db.Column(db.Integer, default=7, comment='自动确认时间（天）')
    bill_type = db.Column(db.Integer, comment='发票类型：0->不开发票；1->电子发票；2->纸质发票')
    bill_header = db.Column(db.String(200), comment='发票抬头')
    bill_content = db.Column(db.String(200), comment='发票内容')
    bill_receiver_phone = db.Column(db.String(32), comment='收票人电话')
    bill_receiver_email = db.Column(db.String(64), comment='收票人邮箱')
    receiver_name = db.Column(db.String(100), nullable=False, comment='收货人姓名')
    receiver_phone = db.Column(db.String(32), nullable=False, comment='收货人电话')
    receiver_post_code = db.Column(db.String(32), comment='收货人邮编')
    receiver_province = db.Column(db.String(32), comment='省份/直辖市')
    receiver_city = db.Column(db.String(32), comment='城市')
    receiver_region = db.Column(db.String(32), comment='区')
    receiver_detail_address = db.Column(db.String(200), comment='详细地址')
    note = db.Column(db.String(500), comment='订单备注')
    confirm_status = db.Column(db.Integer, default=0, comment='确认收货状态：0->未确认；1->已确认')
    delete_status = db.Column(db.Integer, nullable=False, default=0, comment='删除状态：0->未删除；1->已删除')
    payment_time = db.Column(db.BIGINT, comment='支付时间')
    delivery_time = db.Column(db.BIGINT, comment='发货时间')
    receive_time = db.Column(db.BIGINT, comment='确认收货时间')
    comment_time = db.Column(db.BIGINT, comment='最新评价时间')
    gmt_modified = db.Column(db.BIGINT, comment='修改时间')
    create_by = db.Column(db.String(50), comment='创建者')
    modified_by = db.Column(db.String(50), comment='更新者')


class OrderItem(db.Model):
    __tablename__ = 't_order_item'
    __table_args__ = {'comment': '订单详情表'}

    id = db.Column(db.BIGINT, primary_key=True)
    order_id = db.Column(db.BIGINT, comment='订单id')
    order_number = db.Column(db.String(64), index=True, comment='订单编号')
    product_id = db.Column(db.BIGINT, comment='商品id')
    product_spu_id = db.Column(db.BIGINT, comment='商品spuId')
    product_pic = db.Column(db.String(500), comment='商品图片')
    product_name = db.Column(db.String(200), comment='商品名称')
    product_brand = db.Column(db.String(200), comment='商品品牌')
    product_normal_price = db.Column(db.Float(10, 2), comment='正常价格')
    product_price = db.Column(db.Float(10, 2), comment='销售价格')
    product_settlement_price = db.Column(db.Float(10, 2), comment='结算价格')
    product_quantity = db.Column(db.Integer, comment='购买数量')
    product_sku_id = db.Column(db.BIGINT, comment='商品sku编号')
    product_sku_code = db.Column(db.String(50), comment='商品sku条码')
    product_category_id = db.Column(db.BIGINT, comment='商品分类id')
    product_attr = db.Column(db.String(256), comment='实例：商品销售属性:[{"key":"颜色","value":"颜色"},{"key":"容量","value":"4G"}]')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    gmt_modified = db.Column(db.BIGINT, comment='修改时间')
    create_by = db.Column(db.String(50), comment='创建者')
    modified_by = db.Column(db.String(50), comment='更新者')


class OrderRefund(db.Model):
    __tablename__ = 't_order_refund'
    __table_args__ = {'comment': '退单表 '}

    ID = db.Column(db.Integer, primary_key=True, nullable=False, comment='ID')
    refund_no = db.Column(db.String(32), primary_key=True, nullable=False, comment='退单编号')
    order_number = db.Column(db.String(32), nullable=False, index=True, comment='关联订单编号')
    refund_amount = db.Column(db.Float(10, 2), nullable=False, comment='退单金额')
    express_no = db.Column(db.String(32), comment='物流单号')
    merchant_id = db.Column(db.String(50), comment='商家id')
    consignee_realname = db.Column(db.String(32), comment='收货人姓名')
    consignee_telphone = db.Column(db.String(32), comment='联系电话')
    consignee_address = db.Column(db.String(32), comment='收货地址')
    reason = db.Column(db.String(32), nullable=False, comment='退单原因')
    or_status = db.Column(db.Integer, nullable=False, comment='退单状态:0待处理,1处理成功,2处理失败')
    handling_time = db.Column(db.BIGINT, comment='退货处理时间')
    gmt_create = db.Column(db.BIGINT, comment='创建时间(退货申请时间)')
    gmt_modified = db.Column(db.BIGINT, comment='修改时间')
    create_by = db.Column(db.String(50), comment='创建者')
    modified_by = db.Column(db.String(50), comment='更新者')
