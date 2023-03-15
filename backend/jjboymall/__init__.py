# 初始化app
from flask import Flask


def create_app(config_type):
    app = Flask(__name__)
    # 加载配置
    from settings.default import map_config
    app.config.from_object(map_config[config_type])

    # 初始化限制器
    from comment.utils.limitr import limiter
    limiter.init_app(app)

    from comment.utils.request_ware import jwt_request_authorization, loggerHook
    app.before_request(jwt_request_authorization)
    app.after_request(loggerHook)

    # 加载日志处理工具
    from comment.utils.logging import create_logger
    create_logger(app)

    # 初始化sqlalchemy（可连接多个数据库，在init是可指定要用的数据库） 都是在配置里的配置即可 我的关系型数据库在model里实例
    from comment.models import db
    db.init_app(app)

    # 初始化redis数据库连接（可连接多个数据库） 因为这个redis本质是个工具（为了临时存放数据，避免频繁调用后端服务器） 就放到了utils里实例
    from comment.utils.connect_redis import redis_user, redis_cart, redis_index
    redis_user.init_app(app)
    redis_index.init_app(app)
    redis_cart.init_app(app)

    # 加载模块蓝图
    from jjboymall.resources.user import user_bp
    from jjboymall.resources.index import index_bp
    from jjboymall.resources.goods import goods_bp
    from jjboymall.resources.coupon import coupon_bp
    from jjboymall.resources.cart import cart_bp
    from jjboymall.resources.address import address_bp
    from jjboymall.resources.order import order_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(goods_bp)
    app.register_blueprint(coupon_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(order_bp)

    return app


