from urllib.request import urlopen
from urllib.parse import urlencode
from .constants import APIID, APIKEY


def send_sms_code(smscode, phone):
    account = APIID
    password = APIKEY
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。" % smscode
    data = {'account': account, 'password': password, 'content': text, 'mobile': phone, 'format': 'json'}
    req = urlopen(url='https://106.ihuyi.com/webservice/sms.php?method=Submit', data=urlencode(data).encode())
    content = req.read().decode()
    return content
