# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import hashlib
import hmac

from cms.lib import system_code
from cms.lib import utils
from cms.database.data_factory.admin_user import AdminUserDataFactory
from cms.database.data_factory.uuid import UuidDataFactory
from cms.database.redis_key.redis.user import USER_TOKEN
from cms.lib.service import Service
from cms.service.users.check import CheckService


class AdminUserService(Service):

    def __init__(self):
        super(Service, self).__init__()
        self.__check_service = CheckService()

        self.__admin_user_data_factory = AdminUserDataFactory()  # 用户即空间主
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
        admin_user = self.__admin_user_data_factory.get_admin_user_by_account(account)
        if admin_user:
            salt = admin_user.admin_user_salt
            hashed_password = self.get_hashed_password(password, salt)
            saved_hashed_password = admin_user.admin_user_password

            check = self.__compare_passwords(hashed_password, saved_hashed_password)

            if check:
                result = admin_user
            else:
                # 密码错误
                code = system_code.USER_PWD_ERROR
        else:
            # 用户不存在
            code = system_code.USER_NOT_FOUND

        return result, code

    def reset_user_pass(self, user_id, password):

        salt = utils.my_random_string(10)

        result_user_id = self.__admin_user_data_factory.update_admin_user(
                admin_user_id=user_id,
                password=self.get_hashed_password(password, salt),
                salt=salt,
        )

        if result_user_id:
            return result_user_id
        else:
            return None

    def is_user_pass(self, user_id, password):
        result = False
        admin_user = self.__admin_user_data_factory.get_admin_user_by_id(user_id)
        if admin_user:
            salt = admin_user.admin_user_salt
            hashed_password = self.get_hashed_password(password, salt)
            saved_hashed_password = admin_user.admin_user_password

            check = self.__compare_passwords(hashed_password, saved_hashed_password)

            if check:
                result = True

        return result
