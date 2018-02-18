# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import hashlib
import hmac
import random
import string
import time
import ujson as json
from datetime import date
from cms.lib import system_code
from cms.lib.singleton import singleton
from cms.database.data_factory.zone_source import ZoneSourceDataFactory
from cms.lib.service import Service
from cms.service.users.session import SessionService
from cms.service.constants.user import USER_STATUS_NORMAL
from cms.database.redis_key.redis.user import USER_INFO_REDIS_KEY_PRIFEX
from cms.database.redis_key.redis.user import USER_TOKEN
from cms.database.redis_key.redis.user import USER_INFO_STATUS_REDIS_KEY


@singleton
class UserInfoService(Service):
    __session_service = None

    __user_data_factory = None

    def __init__(self):
        super(Service, self).__init__()
        self.__session_service = SessionService()

        self.__user_data_factory = ZoneSourceDataFactory()

    def get_user_info(self, user_id):
        user_info = self.__user_data_factory.get_zone_source_by_id(user_id)
        return user_info

    def get_user(self, user_id):
        result = None
        code = 0
        user = self.__user_data_factory.get_zone_source_by_id(user_id)
        if user and user.zone_source_status == 100:
            result = {
                'user': user,
            }
        else:
            code = system_code.USER_IS_DISABLED

        return result, code

    def get_user_id_by_token_id(self, token_id):
        if not token_id:
            return None

        redis_key = USER_TOKEN + token_id
        result = self.redis.get(redis_key)
        if result:
            self.redis.expire(redis_key, 86400 * 60)
            try:
                result = int(result)
            except Exception, e:
                result = 0
        return result

    def get_current_user(self, session_id, user_id, token):

        if user_id and token:
            user_id = self.get_user_id_by_token_id(token)
            self.__session_service.set_session(session_id, 'user_id', user_id)

            # 把用户状态和用户类型缓存到redis
            user_info_redis_key = USER_INFO_REDIS_KEY_PRIFEX + str(user_id)

            user_status, = self.redis.hmget(
                user_info_redis_key,
                USER_INFO_STATUS_REDIS_KEY
            )

            if not user_status:
                user_auth = self.__user_data_factory.get_zone_source_by_id(user_id)
                if not user_auth:
                    return None

                user_status = user_auth.zone_source_status
                data = {
                    USER_INFO_STATUS_REDIS_KEY: user_status
                }
                self.redis.hmset(user_info_redis_key, data)
                self.redis.expire(user_info_redis_key, 604800)

            if user_status:
                user_status = int(user_status)
            else:
                user_status = 0
            if user_status != USER_STATUS_NORMAL:
                return None

            user_id = int(user_id)
        else:
            user_id = None

        return user_id

    def update_user_info(self, user_id, nickname, qq, mobile, fee_account_name, fee_account_num):

        result_user_id = self.__user_data_factory.update_zone_source(
            source_id=user_id,

            nickname=nickname,
            qq=qq,
            mobile=mobile,
            fee_account_name=fee_account_name,
            fee_account_num=fee_account_num,
        )

        if result_user_id:
            return result_user_id
        else:
            return None
