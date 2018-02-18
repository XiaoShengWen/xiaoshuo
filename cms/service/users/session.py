# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

from cms.lib.singleton import singleton
from cms.lib.service import Service
from uuid import uuid4


@singleton
class SessionService(Service):
    def generage_session_id(self):
        """
        生成session_id
        :return:
        """
        random_str = uuid4().hex[:16]
        return random_str

    def get_session(self, session_id, key):
        session_key = '%s_%s' % ('session', session_id)
        return self.redis_single.hget(session_key, key)

    def set_session(self, session_id, key, value):
        session_key = '%s_%s' % ('session', session_id)
        self.redis_single.hset(session_key, key, value)
        self.redis_single.expire(session_key, 14400)

    def set_incr_session(self, session_id, key, amount=1):
        session_key = '%s_%s' % ('session', session_id)
        num = self.redis_single.hincrby(session_key, key)
        self.redis_single.expire(session_key, 14400)
        return num
