# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from yule.lib import system_code
from yule.database.data_factory.admin_user import AdminUserDataFactory
from yule.lib.service import Service
from yule.service.users.session import SessionService
from yule.database.redis_key.redis.user import USER_INFO_REDIS_KEY_PRIFEX
from yule.database.redis_key.redis.user import USER_TOKEN
from yule.database.redis_key.redis.user import USER_INFO_ROLE_REDIS_KEY


class AdminUserInfoService(Service):

    def __init__(self):
        super(Service, self).__init__()
        self.__session_service = SessionService()

        self.__admin_user_data_factory = AdminUserDataFactory()

    def get_admin_user_info(self, user_id):
        admin_user_info = self.__admin_user_data_factory.get_admin_user_by_id(user_id)
        return admin_user_info

    def get_admin_user(self, user_id):
        result = None
        code = 0
        admin_user = self.__admin_user_data_factory.get_admin_user_by_id(user_id)
        if admin_user:
            result = {
                'admin_user': admin_user,
            }
        else:
            code = system_code.USER_NOT_FOUND

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

            user_role, = self.redis.hmget(
                user_info_redis_key,
                USER_INFO_ROLE_REDIS_KEY
            )

            if not user_role:
                admin_user = self.__admin_user_data_factory.get_admin_user_by_id(user_id)
                if not admin_user:
                    return None

                user_role = admin_user.admin_user_role
                data = {
                    USER_INFO_ROLE_REDIS_KEY: user_role
                }
                self.redis.hmset(user_info_redis_key, data)
                self.redis.expire(user_info_redis_key, 604800)

            user_id = int(user_id)
        else:
            user_id = None

        return user_id

    def update_admin_user_info(self, user_id, nickname, email, mobile):

        result_user_id = self.__admin_user_data_factory.update_admin_user(
                admin_user_id=user_id,
                nickname=nickname,
                email=email,
                mobile=mobile
        )

        if result_user_id:
            return result_user_id
        else:
            return None
