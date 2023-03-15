# # -*- coding: utf-8 -*-
# # import sys
# from comment.utils.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
# # from comment.utils.aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
# from aliyunsdkcore.client import AcsClient
# import uuid
# # from aliyunsdkcore.profile import region_provider
# # from aliyunsdkcore.http import method_type as MT
# # from aliyunsdkcore.http import format_type as FT
#
# """
# 短信业务调用接口示例，版本号：v20170525
#
# Created on 2017-06-12
#
# """
#
# REGION = "cn-shanghai"
# SIGN_NAME = '猪猪侠'
# TEMPLATE_id = 'SMS_193519304'
# ACCESS_KEY_ID = ''
# ACCESS_KEY_SECRET = ''
# acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
#
# '''
# region:        哪个地区的服务商
# phone_numbers  发送短信的目标手机号码
# sign_name      短信的签名
# template_id    申请成功之后模板ID
# '''
#
#
# def send_sms(phone_numbers, code):
#     business_id = uuid.uuid1()  # 通过UUID生成一个随机的ID
#
#     smsRequest = SendSmsRequest.SendSmsRequest()
#     # 申请的短信模板编码,必填
#     smsRequest.set_TemplateCode(TEMPLATE_id)
#
#     # 短信模板变量参数
#     if code is not None:
#         params = "{\"code\":\"" + code + "\"}"  # 发送的手机验证码
#         smsRequest.set_TemplateParam(params)
#
#     # 设置业务请求流水号，必填。可通过uuid来生成（没意义但必须有）
#     smsRequest.set_OutId(business_id)
#
#     # 短信签名
#     smsRequest.set_SignName(SIGN_NAME)
#
#     # 数据提交方式 默认post
#     # smsRequest.set_method(MT.POST)
#
#     # 数据提交格式 默认json
#     # smsRequest.set_accept_format(FT.JSON)
#
#     # 短信发送的号码列表，必填。
#     smsRequest.set_PhoneNumbers(phone_numbers)
#
#     # 调用短信发送接口，返回json
#     smsResponse = acs_client.do_action_with_exception(smsRequest)
#
#     # TODO 业务处理
#
#     return smsResponse.decode('utf-8')
#
#
# if __name__ == '__main__':
#     # 只需要传目标手机号 和 验证码
#     result = send_sms("18684640986", '123453')
#     print(result)
