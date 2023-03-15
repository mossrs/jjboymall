from comment.models import db
from sqlalchemy.util._collections import AbstractKeyedTuple
import datetime
import decimal

# 这是一个 AbstractKeyedTuple 对象，它拥有一个 keys() 方法。我们可以通过这个方法将查询结果转换为字典，需要传到前端展示只需要将其装换为json格式即可。
# 示例：data = [dict(zip(result.keys(), result)) for result in results]


def datas_to_dict(res_obj):
    if isinstance(res_obj[0], AbstractKeyedTuple):
        return data_format([dict(zip(result.keys(), result)) for result in res_obj])
    elif isinstance(res_obj[0], db.Model):
        [item.__dict__.pop("_sa_instance_state") for item in res_obj]
        return data_format([item.__dict__ for item in res_obj])
    elif isinstance(res_obj[0], dict):
        return data_format(res_obj)
    else:
        return None


def data_to_dict(res_obj):
    if isinstance(res_obj, dict):
        return data_format(res_obj)
    elif isinstance(res_obj, AbstractKeyedTuple):
        return data_format(dict(zip(res_obj.keys(), res_obj)))
    elif isinstance(res_obj, db.Model):
        res_obj.__dict__.pop("_sa_instance_state")
        return data_format(res_obj.__dict__)
    else:
        return None


def data_format(res):

    def json_format(item):
        for key in item.keys():
            if isinstance(item[key], datetime.datetime) or isinstance(item[key], datetime.date):
                item[key] = str(item[key])
            if isinstance(item[key], decimal.Decimal):
                item[key] = float(item[key])
        return item

    if isinstance(res, dict):
        return json_format(res)
    elif isinstance(res, list):
        for i in res:
            return [json_format(i) for i in res]



