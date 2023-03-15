from logging import Formatter, handlers, getLogger, StreamHandler
from flask import request
import os


class RequestShoppingFormatter(Formatter):
    """
    自定义的日志输出格式 可以定义一些父类里没有的格式  看源码 这个类就是重写一些父类里没有的格式
    最后要连带重写的和原来的返回这个函数调用
    """

    def format(self, record):
        # 在日志中记录请求地址
        record.url = request.url
        # 在日志中记录客户端地址
        record.remote_addr = request.remote_addr
        return super().format(record)


# 定制logger对象 可定制多个
def create_logger(app):
    logging_level = app.config['LOGGING_LEVEL']
    logging_dir = app.config['LOGGING_FILE_DIR']
    logging_max_bytes = app.config['LOGGING_FILE_MAX_BYTES']
    logging_backup = app.config['LOGGING_FILE_BACKUP']

    # 文件log的输出格式
    request_formatter = RequestShoppingFormatter('[%(asctime)s] %(remote_addr)s 请求 %(url)s \t %(levelname)s 在 %('
                                                 'module)s %(lineno)d : %(message)s')

    # 检索日志文件是否存在
    if not os.path.isdir(logging_dir):
        os.mkdir(logging_dir)

    # 创建文件loghandler
    # join是连接文件目录和文件  RotatingFileHandler是分文件流 即文件大小超过指定的容量时自动在生成一个文件存储
    flask_file_handler = handlers.RotatingFileHandler(filename=os.path.join(logging_dir, 'logging.log'),
                                                      # 可指定文件名字
                                                      maxBytes=logging_max_bytes,
                                                      backupCount=logging_backup, encoding='utf-8')

    # 给当前的handler设置格式
    flask_file_handler.setFormatter(request_formatter)

    # 创建 console_handler
    # 使用StreamHandler() 来创建
    flask_console_handler = StreamHandler()
    flask_console_handler.setFormatter(Formatter('[%(asctime)s] %(levelname)s '
                                                 '%(module)s %(lineno)d %(message)s'))

    # 创建一个logger对象 这个name是你app运行的父目录名字 如果不归属任何一个目录那就是根目录root
    flask_logger = getLogger('shopping')
    flask_logger.setLevel(logging_level)
    flask_logger.addHandler(flask_file_handler)
    # 当项目运行环境是debug 才使用控制台输出
    # 一个logger对象可以加多个个handler
    if app.debug:
        flask_logger.addHandler(flask_console_handler)



