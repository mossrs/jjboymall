# JJBoyMall入口

# 将该项目的运行环境添加到系统环境变量中
import os
import sys
path = os.path.dirname(sys.path[0])
if path and path not in sys.path:
    sys.path.append(path)

from jjboymall import create_app
app = create_app('develop')


if __name__ == '__main__':
    app.run()
