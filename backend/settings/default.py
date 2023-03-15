# 负责整个项目的配置信息
import os

class Config:
    # 配置数据库
    URI = 'mysql+pymysql://root:root@localhost:3306/jjboymall?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要追踪数据修改

    # 配置日志
    # 当你的日志等级只要大于这个等级就会输出
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FILE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')  # 指定日志文件的目录
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024                  # 指定每个日志文件的容量
    LOGGING_FILE_BACKUP = 10  # 日志文件的总数

    # 限流器采用redis保存数据  保存客户每次发送短信得到的验证码（因为客户可能多次发送，所以使用限流器）
    # 这个配置url的会自动连接（源码里解释）
    RATELIMIT_STORAGE_URL = 'redis://127.0.0.1:6379/0'
    # 限制策略：移动窗口（时间窗口会自动变化）即会自动跟踪你发短信的起始时间和你规定的发送频次是否过了频次才能再次发送，来限制
    RATELIMIT_STORAGE = 'moving-window'

    # redis数据库的连接地址 这个数据库是来保存客户验证时填写的验证码（并进行匹配是否成功）
    REDIS1_URL = 'redis://127.0.0.1:6379/1'
    REDIS2_URL = 'redis://127.0.0.1:6379/2'
    REDIS3_URL = 'redis://127.0.0.1:6379/3'


# 开发环境下配置信息
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 打印sql语句


# 生产环境中配置信息
class ProductConfig(Config):
    pass


# 把两个不同环境的配置信息和字符串映射起来
map_config = {
    'develop': DevelopmentConfig,
    'product': ProductConfig
}
