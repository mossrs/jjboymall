from comment.models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 用户模型类
class User(db.Model):
    __tablename__ = 't_user'
    # BIGINT是double类型范围更大
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    # doc= 就是注释 你也可以在外面注释 其实没啥用
    username = db.Column(db.String(64), doc='用户名')
    # 数据库中存放的是加密后的密文 采用flask提供的哈希算法（生成一个128位的密文）
    password = db.Column(db.String(256), doc='密码')
    email = db.Column(db.String(64), doc='邮箱')
    phone = db.Column(db.String(11), doc='手机号')
    nick_name = db.Column(db.String(64), doc='昵称')
    icon = db.Column(db.String(4096), doc='用户头像图片')
    status = db.Column(db.Integer, doc='用户状态')
    login_time = db.Column(db.DateTime, default=datetime.now(), doc='登陆时间')
    create_time = db.Column(db.DateTime, default=datetime.now(), doc='注册时间')
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), doc='修改时间')
    note = db.Column(db.String(64), doc='备注')

    @property
    def pwd(self):
        # 使用property将pwd变成实例属性 然后返回模型明文密码
        return self.password

    # 是pwd属性的一个setter方法（传pwd属性返回的明文密码）
    @pwd.setter
    def pwd(self, x_passwd):
        # 根据一个明文密码生成一个密文（传的就是模型明文,数据库存的是密文防止客户资料泄露）
        # 这个generate_password_hash是通过哈希算法返回一个128位的密文（然后我又赋值给了User模型的password属性，所以数据库存的就是密文）
        self.password = generate_password_hash(x_passwd)

    def check_passwd(self, x_passwd):
        # 登录时通过传明文来校验是否与数据库的密文是否匹配
        # check_password_hash函数第一个参数: 密文 第二个参数是: 明文 成功返回True
        return check_password_hash(self.password, x_passwd)
