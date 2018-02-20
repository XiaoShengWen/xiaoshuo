# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import hashlib
import hmac
import string
import logging
import traceback

from datetime import datetime
from datetime import date
from yule.lib import system_code
from yule.lib import utils
from yule.lib.singleton import singleton
from yule.database.data_factory.zone_source import ZoneSourceDataFactory
from yule.database.data_factory.uuid import UuidDataFactory
from yule.database.redis_key.redis.user import USER_TOKEN
from yule.lib.service import Service
from yule.service.users.check import CheckService
from yule.service.constants.user import USER_STATUS_NORMAL
from yule.service.constants.user import USER_STATUS_DISABLED
from yule.service.constants.user import USER_DEFAULT_FEE_MODE
from yule.service.constants.user import USER_SOURCE_REGISTE
from yule.service.constants.user import USER_REGISTE_DEFAULT_MANAGER


@singleton
class UserService(Service):
    __check_service = None

    __user_data_factory = None
    __uuid_data_factory = None

    def __init__(self):
        super(Service, self).__init__()
        self.__check_service = CheckService()

        self.__user_data_factory = ZoneSourceDataFactory()  # 用户即空间主
        self.__uuid_data_factory = UuidDataFactory()

    @classmethod
    def get_hashed_password(cls, password, salt):
        # TODO decide if password is utf-8
        return hmac.new(str(salt), password.encode('utf-8'), hashlib.sha256).hexdigest()

    @classmethod
    def __compare_passwords(cls, a, b):
        return utils.compare_digest(a, b)

    @classmethod
    def __generate_reset_token(cls, channel='website'):
        if channel == 'website':
            token = utils.my_random_string(30)
        else:
            token = utils.my_random_string(32)
        return token

    def create_user_token(self, user_id, device_id=None, channel='website'):
        if not user_id:
            return False

        token = self.__generate_reset_token(channel)

        if device_id:
            redis_key = USER_TOKEN + (device_id)
            result = self.redis.set(redis_key, user_id)

        redis_key = USER_TOKEN + (token)
        result = self.redis.setex(redis_key, 86400 * 60, user_id)

        if result:
            return token
        else:
            return False

    def login(self, account, password):
        code = 0
        result = None
        user_auth = self.__user_data_factory.get_zone_source_by_account(account)
        if user_auth:
            salt = user_auth.zone_source_salt
            hashed_password = self.get_hashed_password(password, salt)
            saved_hashed_password = user_auth.zone_source_password

            check = self.__compare_passwords(hashed_password, saved_hashed_password)

            if check:
                if user_auth.zone_source_status == USER_STATUS_NORMAL:
                    result = user_auth
                    # 记录最后登录时间 ip
                    # self.__user_data_factory.save_last_login_ip_and_time(user_auth.user_id, remote_ip)
                else:
                    # 用户被禁用
                    code = system_code.USER_IS_DISABLED
            else:
                # 密码错误
                code = system_code.USER_PWD_ERROR
        else:
            # 用户不存在
            code = system_code.USER_NOT_FOUND

        return result, code

    def create_user(self, account, password, nickname, email, qq, mobile, fee_account_name, fee_account_num):
        # user_id = self.__uuid_data_factory.get_short_uuid()

        salt = utils.my_random_string(10)

        user_id = self.__user_data_factory.create_zone_source(
            # user_id=user_id,

            account=account,
            password=self.get_hashed_password(password, salt),
            nickname=nickname,
            salt=salt,
            email=email,
            qq=qq,
            mobile=mobile,
            fee_mode=USER_DEFAULT_FEE_MODE,
            fee_account_name=fee_account_name,
            fee_account_num=fee_account_num,
            source=USER_SOURCE_REGISTE,
            user_status=USER_STATUS_DISABLED,
            manager=USER_REGISTE_DEFAULT_MANAGER,
        )

        if user_id:
            token = self.create_user_token(user_id)
            return user_id, token
        else:
            return None, None

    def reset_user_pass(self, user_id, password):

        salt = utils.my_random_string(10)

        result_user_id = self.__user_data_factory.update_zone_source(
            source_id=user_id,

            password=self.get_hashed_password(password, salt),
            salt=salt,
        )

        if result_user_id:
            return result_user_id
        else:
            return None

    def is_user_pass(self, user_id, password):
        result = False
        user_auth = self.__user_data_factory.get_zone_source_by_id(user_id)
        if user_auth:
            salt = user_auth.zone_source_salt
            hashed_password = self.get_hashed_password(password, salt)
            saved_hashed_password = user_auth.zone_source_password

            check = self.__compare_passwords(hashed_password, saved_hashed_password)

            if check:
                if user_auth.zone_source_status == USER_STATUS_NORMAL:
                    result = True

        return result
