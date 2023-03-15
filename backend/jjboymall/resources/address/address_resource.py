from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from comment.utils.data_format import datas_to_dict
from comment.models import db
from comment.models.address import Address
from comment.models.user import User
from comment.utils.decorators import login_required


class User_Address(Resource):
    """
        用户地址管理
    """

    method_decorators = {
        'post': [login_required],
        'delete': [login_required],
        'put': [login_required]
    }

    def __init__(self):
        self.user_id = g.user_id

    # 查询用户地址列表
    def get(self):
        rp = RequestParser()
        rp.add_argument('username', required=True)
        args = rp.parse_args()
        username = args.username
        res = Address.query.join(User, Address.login_user == username).\
            filter(Address.login_user == username, Address.enabled == 0).all()
        if res:
            res_data = datas_to_dict(res)
            return res_data
        else:
            return {'message': '', 'code': 201}

    # 新增用户地址
    def post(self):
        rp = RequestParser()
        rp.add_argument('address', required=True)
        rp.add_argument('area', required=True)
        rp.add_argument('city', required=True)
        rp.add_argument('defaultAddress', required=True)
        rp.add_argument('loginUser', required=True)
        rp.add_argument('province', required=True)
        rp.add_argument('recipient', required=True)
        rp.add_argument('telephone', required=True)
        args = rp.parse_args()
        address = args.address
        area = args.area
        city = args.city
        defaultAddress = 1 if args.defaultAddress == 'true' else 0
        loginUser = args.loginUser
        province = args.province
        recipient = args.recipient
        telephone = args.telephone

        if defaultAddress:
            self.set_default_false(loginUser)
        add = Address(login_user=loginUser, recipient=recipient, address=address, area=area, city=city, default_address=
                      defaultAddress, province=province, telephone=telephone, enabled=1)
        db.session.add(add)
        db.session.commit()
        return {'msg': 'OK'}

    # 更新用户地址
    def put(self):
        rp = RequestParser()
        rp.add_argument('address', required=True)
        rp.add_argument('area', required=True)
        rp.add_argument('city', required=True)
        rp.add_argument('defaultAddress', required=True)
        rp.add_argument('loginUser', required=True)
        rp.add_argument('province', required=True)
        rp.add_argument('recipient', required=True)
        rp.add_argument('telephone', required=True)
        args = rp.parse_args()
        address = args.address
        area = args.area
        city = args.city
        defaultAddress = 1 if args.defaultAddress == 'true' else 0
        loginUser = args.loginUser
        province = args.province
        recipient = args.recipient
        telephone = args.telephone

        if defaultAddress:
            self.set_default_false(loginUser)
        res = Address.query.filter(Address.login_user == loginUser, Address.id == self.user_id)
        if res:
            res.update({'address': address, 'area': area, 'city': city, 'default_address': defaultAddress,
                        'login_user': loginUser, 'province': province, 'recipient': recipient, 'telephone': telephone})
        db.session.commit()
        return {'msg': 'OK'}

    # 删除用户地址(默认删全部)
    def delete(self):
        Address.query.filter(Address.id == self.user_id).delete()
        db.session.commit()
        return {'msg': 'Delete Finish'}

    @staticmethod
    def set_default_false(username):
        res = Address.query.filter(Address.login_user == username)
        if res:
            res.first().default_address = 1
            db.session.commit()







