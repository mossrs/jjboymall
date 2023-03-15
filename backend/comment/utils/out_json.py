from json import dumps
from flask_restful.utils import PY3
from flask import make_response, current_app

"""
    前后端统一
        当用户数据正常时 返回msg 不用写状态码
        当用户数据不正常时 返回message 加状态码    
"""


def output_json(data, code, headers=None):
    if 'message' not in data:
        data = {
            'code': 200,
            'data': data
        }
    settings = current_app.config.get('RESTFUL_JSON', {})
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    dumped = dumps(data, **settings)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp

