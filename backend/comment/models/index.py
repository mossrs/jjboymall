from comment.models import db
from sqlalchemy import text


class Product(db.Model):
    __tablename__ = 't_product'
    __table_args__ = {'comment': '商品表'}
    id = db.Column(db.BigInteger, primary_key=True, comment='商品主键id')
    product_no = db.Column(db.String(64), comment='商品编号')
    product_name = db.Column(db.String(255), comment='商品名称')
    rel_tenant_id = db.Column(db.BigInteger, comment='商户id')
    rel_default_sku_id = db.Column(db.BigInteger, comment='默认SKU')
    rel_category1_id = db.Column(db.BigInteger, comment='一级类目')
    rel_category2_id = db.Column(db.BigInteger, comment='二级类目')
    rel_category3_id = db.Column(db.BigInteger, comment='三级类目')
    spec_options = db.Column(db.String(60), comment='规格选项id集合')
    price = db.Column(db.Numeric(11, 2), comment='商城价')
    default_pic = db.Column(db.String(512), comment='商品图片')
    album_pics = db.Column(db.Text, comment='商品组图,加上默认主图，最多允许5张图，逗号分割')
    sales_num = db.Column(db.Integer, comment='销量')
    detail_desc = db.Column(db.String(512), comment='商品详情描述')
    publish_status = db.Column(db.SmallInteger, comment='上架状态：0->下架；1->上架')
    detail_html = db.Column(db.String(512), comment='商品详情web端页面，基本以图为主，富文本HTML样式')
    enabled = db.Column(db.SmallInteger, nullable=False, comment='逻辑删除 0-未删除，1-删除')
    gmt_create = db.Column(db.BigInteger, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, comment='更新时间')
    modified_uid = db.Column(db.String(50), comment='更新人uid')
    create_uid = db.Column(db.String(50), comment='创建人uid')
    create_uname = db.Column(db.String(255), comment='创建人昵称')
    modified_uname = db.Column(db.String(255), comment='更新人昵称')


class Category(db.Model):
    __tablename__ = 't_category'
    __table_args__ = {'comment': '商品分类表'}
    id = db.Column(db.BigInteger, primary_key=True)
    level = db.Column(db.SmallInteger, server_default=text("'1'"), comment='层级')
    parent_id = db.Column(db.BigInteger, server_default=text("'0'"), comment='父id')
    name = db.Column(db.String(255), comment='中文')
    en = db.Column(db.String(255), comment='英文')
    sort = db.Column(db.SmallInteger, comment='排序，暂未使用')
    catid = db.Column(db.Integer, comment='类目id，关联pid使用')
    catid_use = db.Column(db.SmallInteger, default=0, comment='是否使用catid查询')
    query_t = db.Column(db.String(255), comment='淘宝查询')
    query_t_use = db.Column(db.SmallInteger, default=1, comment='是否使用query')
    weight = db.Column(db.Float, comment='类目单元配重')
    status = db.Column(db.SmallInteger, default=1, comment='状态')
    gmt_create = db.Column(db.BigInteger, nullable=False, default=0, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, nullable=False, default=0, comment='更新时间')
    create_uid = db.Column(db.String(64), nullable=False, default=0, comment='创建人uid')
    create_uname = db.Column(db.String(64), nullable=False, default=0, comment='创建人昵称')
    modified_uid = db.Column(db.String(64), nullable=False, default=0, comment='更新人uid')
    modified_uname = db.Column(db.String(64), nullable=False, default=0, comment='更新人昵称')
    enabled = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否删除:0-未删除;1-删除')
    merchant_id = db.Column(db.String(32), comment='商户ID')


class HomeNewProduct(db.Model):
    # 这个__table_args__是当在同一数据库中(database)不同模式（schema）中指定对应的表或其他内容附加的参数（即整个表的注释）
    __tablename__ = 't_home_new_product'
    __table_args__ = {'comment': '新品推荐表'}
    id = db.Column(db.BigInteger, primary_key=True, comment='主键')
    product_id = db.Column(db.BigInteger, comment='商口ID')
    product_name = db.Column(db.String(128), comment='商口标题')
    recommend_status = db.Column(db.Integer, comment='推荐状态:0-未推荐;1-推荐')
    sort = db.Column(db.Integer, comment='排序')
    gmt_create = db.Column(db.BigInteger, nullable=False, default=0, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, nullable=False, default=0, comment='更新时间')
    create_uid = db.Column(db.String(64), nullable=False, default=0, comment='创建人uid')
    create_uname = db.Column(db.String(64), nullable=False, default=0, comment='创建人昵称')
    modified_uid = db.Column(db.String(64), nullable=False, default=0, comment='更新人uid')
    modified_uname = db.Column(db.String(64), nullable=False, default=0, comment='更新人昵称')
    enable = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否删除:0-未删除;1-删除')
    merchant_id = db.Column(db.String(32), comment='商户ID')


class HomeRecommendProduct(db.Model):
    __tablename__ = 't_home_recommend_product'
    __table_args__ = {'comment': '人气热搜表'}
    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, comment='商品ID')
    product_name = db.Column(db.String(64), comment='商品名称')
    recommend_status = db.Column(db.Integer, comment='推荐状态')
    sort = db.Column(db.Integer, comment='排序')
    gmt_create = db.Column(db.BigInteger, nullable=False, default=0, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, nullable=False, default=0, comment='更新时间')
    create_uid = db.Column(db.String(64), nullable=False, default=0, comment='创建人uid')
    create_uname = db.Column(db.String(64), nullable=False, default=0, comment='创建人昵称')
    modified_uid = db.Column(db.String(64), nullable=False, default=0, comment='更新人uid')
    modified_uname = db.Column(db.String(64), nullable=False, default=0, comment='更新人昵称')
    enable = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否删除:0-未删除;1-删除')
    merchant_id = db.Column(db.Integer, comment='商户ID')


class CmsSubject(db.Model):
    __tablename__ = 't_cms_subject'
    __table_args__ = {'comment': '专题表'}
    id = db.Column(db.BigInteger, primary_key=True)
    subject_category_id = db.Column(db.BigInteger, comment='专题分类id')
    title = db.Column(db.String(100), comment='专题标题')
    pic = db.Column(db.String(500), comment='专题主图')
    product_count = db.Column(db.Integer, comment='关联产品数量')
    recommend_status = db.Column(db.Integer, comment='推荐状态')
    create_time = db.Column(db.DateTime)
    collect_count = db.Column(db.Integer)
    read_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    album_pics = db.Column(db.Text, comment='画册图片用逗号分割')
    description = db.Column(db.String(1000))
    show_status = db.Column(db.Integer, comment='显示状态：0->不显示；1->显示')
    content = db.Column(db.Text)
    forward_count = db.Column(db.Integer, comment='转发数')
    hot_words = db.Column(db.String(500), comment='专题热词,聚类出频率最高的前10个词,逗号分割')
    gmt_create = db.Column(db.BigInteger, nullable=False, default=0, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, nullable=False, default=0, comment='更新时间')
    create_uid = db.Column(db.String(64), nullable=False, default=0, comment='创建人uid')
    create_uname = db.Column(db.String(64), nullable=False, default=0, comment='创建人昵称')
    modified_uid = db.Column(db.String(64), nullable=False, default=0, comment='更新人uid')
    modified_uname = db.Column(db.String(64), nullable=False, default=0, comment='更新人昵称')
    enable = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否删除:0-未删除;1-删除')
    merchant_id = db.Column(db.Integer, comment='商户ID')


class CmsSubjectCategory(db.Model):
    __tablename__ = 't_cms_subject_category'
    __table_args__ = {'comment': '专题分类表'}
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    icon = db.Column(db.String(500), comment='分类图标')
    subject_count = db.Column(db.Integer, comment='专题数量')
    show_status = db.Column(db.Integer)
    sort = db.Column(db.Integer)
    gmt_create = db.Column(db.BigInteger, nullable=False, default=0, comment='创建时间')
    gmt_modified = db.Column(db.BigInteger, nullable=False, default=0, comment='更新时间')
    create_uid = db.Column(db.String(64), nullable=False, default=0, comment='创建人uid')
    create_uname = db.Column(db.String(64), nullable=False, default=0, comment='创建人昵称')
    modified_uid = db.Column(db.String(64), nullable=False, default=0, comment='更新人uid')
    modified_uname = db.Column(db.String(64), nullable=False, default=0, comment='更新人昵称')
    enable = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否删除:0-未删除;1-删除')
    merchant_id = db.Column(db.Integer, comment='商户ID')


class CmsSubjectProductRelation(db.Model):
    __tablename__ = 't_cms_subject_product_relation'
    __table_args__ = {'comment': '专题商品关系表'}
    id = db.Column(db.BigInteger, primary_key=True)
    subject_id = db.Column(db.BigInteger)
    product_id = db.Column(db.BigInteger)
