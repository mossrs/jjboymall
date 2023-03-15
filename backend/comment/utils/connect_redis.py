from flask_redis import FlaskRedis

# 创建redis数据库的客户端连接，后面是配置路径
redis_user = FlaskRedis(config_prefix='REDIS1')
redis_index = FlaskRedis(config_prefix='REDIS2')
redis_cart = FlaskRedis(config_prefix='REDIS3')


