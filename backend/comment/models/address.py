from comment.models import db


class Address(db.Model):
    __tablename__ = 't_address'
    __table_args__ = {'comment': '用户地址'}

    id = db.Column(db.BIGINT, primary_key=True, comment='主键id')
    login_user = db.Column(db.String(64), comment='当前登录用户名称')
    recipient = db.Column(db.String(64), comment='收件人')
    province = db.Column(db.String(64), comment='省')
    city = db.Column(db.String(64), comment='市')
    area = db.Column(db.String(64), comment='区')
    address = db.Column(db.String(100), comment='详细地址')
    telephone = db.Column(db.String(64), comment='手机号码')
    default_address = db.Column(db.Integer, comment='默认收货地址 1-是,0-否')
    enabled = db.Column(db.Integer, comment='逻辑删除 1-已删除,0-未删除')
    gmt_create = db.Column(db.BIGINT, comment='创建时间')
    gmt_modified = db.Column(db.BIGINT, comment='更新时间')
