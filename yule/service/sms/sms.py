# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import hmac
import hashlib
import string
import random
import urllib
import ujson as json

from tornado import gen
from datetime import datetime
from yule.lib import http
from yule.lib.service import Service
from yule.lib.singleton import singleton
from yule.service.users.session import SessionService

from yule.service.constants.sms import TYPE_RESETPASS
from yule.service.constants.sms import TYPE_REGISTER
from yule.service.constants.sms import SMS_TEMPLATE_78700021

from yule.database.redis_key.redis_single.sms import SMS_CODE
from yule.database.redis_key.redis_single.sms import SMS_MOBILE_NUM
from yule.database.redis_key.redis_single.sms import SMS_TIMES


@singleton
class SmsService(Service):
    __session_service = None

    def __init__(self):
        super(Service, self).__init__()
        self.__session_service = SessionService()

    @classmethod
    def generate_verification_code(cls, number=6):
        """
        生成指定位数验证码
        :param number: 位数
        :return:
        """
        return ''.join([random.choice(string.digits) for x in range(number)])

    @gen.coroutine
    def send_verification_code(self, phone, sms_type, session_id):
        """
        :param phone: 手机号
        :param sms_type: 短信类型
        :param session_id: session id
        :return:
        """
        if sms_type == TYPE_REGISTER:
            result = yield self.__register(session_id, phone)
        elif sms_type == TYPE_RESETPASS:
            result = False
        else:
            result = False

        raise gen.Return(result)

    def check_verification_code(self, session_id, phone, code):
        """
        验证短信
        :param session_id:
        :param phone:
        :param code:
        :return:
        """
        sms_code = self.__session_service.get_session(session_id, SMS_CODE)
        mobile_num = self.__session_service.get_session(session_id, SMS_MOBILE_NUM)

        if sms_code and mobile_num and phone == mobile_num and code == sms_code:
            return True
        else:
            return False

    @gen.coroutine
    def send_sms_to_aliyun(self, sms_param, mobile, sms_template=None):
        """
        通过阿里服务发送短信
        :param sms_param: 验证码参数
        :param mobile: 手机号
        :param sms_template: 短信模板
        :return:
        """

        if not all([sms_param, mobile, sms_template]):
            raise gen.Return(False)

        url = 'http://gw.api.taobao.com/router/rest'

        data = {
            'method': 'alibaba.aliqin.fc.sms.num.send',
            'app_key': '23266160',
            'timestamp': datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            'v': '2.0',
            'sign_method': 'hmac',
            'format': 'json',
            'sms_type': 'normal',
            'sms_free_sign_name': u'第一弹',
            'sms_param': json.dumps(sms_param),
            'rec_num': mobile,
            'sms_template_code': sms_template,
        }

        # 计算签名
        all_arguments = []
        for key in data:
            all_arguments.append(key + data[key])

        all_arguments.sort()

        # 中文排序的问题，待解决
        sign_str = ''.join(all_arguments)
        # sign_str.replace('sms_free_sign_name', 'sms_free_sign_name第一弹')

        sig = hmac.new('a7acc795929dd5d8486d4140969d96d6', sign_str.encode('utf-8'), hashlib.md5).hexdigest()
        sig = sig.upper()

        data['sign'] = sig
        data['sms_free_sign_name'] = '第一弹'  # 不然后面会有编码问题
        result = False

        body = urllib.urlencode(data)

        response_body = yield http.send_http_request(url, method="POST", body=body)

        if not response_body.get('error_response'):
            if response_body['alibaba_aliqin_fc_sms_num_send_response']['result']['success']:
                result = True

        raise gen.Return(result)

    @gen.coroutine
    def __register(self, session_id, phone):
        code = self.generate_verification_code(6)

        self.__session_service.set_session(session_id, SMS_CODE, code)
        self.__session_service.set_session(session_id, SMS_MOBILE_NUM, phone)

        sms_times = self.__session_service.set_incr_session(session_id, SMS_TIMES)

        if sms_times > 10:
            raise gen.Return(False)
        else:
            sms_param = {'code': code}
            result = yield self.send_sms_to_aliyun(sms_param, phone, SMS_TEMPLATE_78700021)
            raise gen.Return(result)
