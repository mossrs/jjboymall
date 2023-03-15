from comment.models import db


class SkuStock(db.Model):
    __tablename__ = 't_sku_stock'
    __table_args__ = {'comment': 'SKU'}

    id = db.Column(db.BIGINT, primary_key=True, comment='SKU主键id')
    sku_no = db.Column(db.String(255), comment='SKU编号')
    rel_product_id = db.Column(db.BIGINT, comment='商品id')
    title = db.Column(db.String(255), comment='商品标题')
    sell_point = db.Column(db.String(255), comment='卖点')
    price = db.Column(db.Float, comment='商品价格')
    num = db.Column(db.Integer, comment='库存数量')
    lock_stock_num = db.Column(db.Integer, comment='冻结库存数量')
    version = db.Column(db.Integer, comment='库存版本')
    image = db.Column(db.String(512), comment='商品照片')
    spec_hash = db.Column(db.String(255), comment='规格哈希值')
    spec = db.Column(db.String(255), comment='规格集合')
    option_ids = db.Column(db.String(255), comment='规格选项id集合')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    gmt_modified = db.Column(db.BIGINT, comment='更新时间')
    enabled = db.Column(db.Integer, comment='逻辑删除 0-未删除，1-删除')
    modified_uid = db.Column(db.String(50), comment='更新人uid')
    create_uid = db.Column(db.String(50), comment='创建人uid')
    modified_uname = db.Column(db.String(255), comment='更新人昵称')
    create_uname = db.Column(db.String(255), comment='创建人昵称')


class SpecType(db.Model):
    __tablename__ = 't_spec_type'
    __table_args__ = {'comment': '商品规格类型表'}

    id = db.Column(db.BIGINT, primary_key=True, comment='规格类别id')
    name = db.Column(db.String(50), comment='规格类别名称')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    gmt_modified = db.Column(db.BIGINT, comment='更新时间')
    enabled = db.Column(db.Integer, comment='逻辑删除 0-未删除，1-删除')
    modified_uid = db.Column(db.String(50), comment='更新人uid')
    create_uid = db.Column(db.String(50), comment='创建人uid')
    modified_uname = db.Column(db.String(255), comment='更新人昵称')
    create_uname = db.Column(db.String(255), comment='创建人昵称')


class Specification(db.Model):
    __tablename__ = 't_specification'
    __table_args__ = {'comment': '商品规格表'}

    id = db.Column(db.BIGINT, primary_key=True, comment='规格主键')
    name = db.Column(db.String(50), comment='规格名称')
    rel_category_id = db.Column(db.BIGINT, comment='类目id')
    rel_spec_type_id = db.Column(db.BIGINT, comment='规格分类id')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    gmt_modified = db.Column(db.BIGINT, comment='更新时间')
    enabled = db.Column(db.Integer, comment='逻辑删除 0-未删除，1-删除')
    modified_uid = db.Column(db.String(50), comment='更新人uid')
    create_uid = db.Column(db.String(50), comment='创建人uid')
    modified_uname = db.Column(db.String(255), comment='更新人昵称')
    create_uname = db.Column(db.String(255), comment='创建人昵称')
    type = db.Column(db.Integer, default=0, comment='规格属性的类型；0->规格；1->参数')


class SpecificationOption(db.Model):
    __tablename__ = 't_specification_option'
    __table_args__ = {'comment': '规格项'}

    id = db.Column(db.BIGINT, primary_key=True, comment='规格项主键id')
    name = db.Column(db.String(50), comment='规格项名称')
    rel_spec_id = db.Column(db.BIGINT, comment='规格id')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    gmt_modified = db.Column(db.BIGINT, comment='更新时间')
    enabled = db.Column(db.Integer, comment='逻辑删除 0-未删除，1-删除')
    modified_uid = db.Column(db.String(50), comment='更新人uid')
    create_uid = db.Column(db.String(50), comment='创建人uid')
    modified_uname = db.Column(db.String(255), comment='更新人昵称')
    create_uname = db.Column(db.String(255), comment='创建人昵称')


class ProductFullReduction(db.Model):
    __tablename__ = 't_product_full_reduction'
    __table_args__ = {'comment': '商品满减表'}

    id = db.Column(db.BIGINT, primary_key=True, comment='主键id')
    product_id = db.Column(db.BIGINT, comment='商品id')
    full_price = db.Column(db.Float(10, 2), comment='商品满足金额')
    reduce_price = db.Column(db.Float(10, 2), comment='商品减少金额')
    start_time = db.Column(db.BIGINT, comment='开始时间')
    end_time = db.Column(db.BIGINT, comment='结束时间')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    create_uid = db.Column(db.String(50), comment='创建人id')
    create_uname = db.Column(db.String(255), comment='创建人昵称')
    gmt_modified = db.Column(db.BIGINT, comment='更新时间')
    modified_uid = db.Column(db.String(50), comment='更新人id')
    modified_uname = db.Column(db.String(255), comment='更新人昵称')
