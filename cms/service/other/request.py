# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import time
from cms.lib.service import Service
from cms.lib.singleton import singleton
from cms.database.redis_key.redis_cache.request import USER_REQUEST
from cms.database.redis_key.redis_cache.request import USER_REQUEST_LIMIT


@singleton
class RequestService(Service):
    def get_remain_request(self, remote_ip, post_id):
        redis_key = USER_REQUEST_LIMIT + remote_ip
        has_limit = self.redis_cache.get(redis_key)
        if not has_limit:
            redis_key = USER_REQUEST + remote_ip + '_' + str(int(time.time()) / 10)
            pipe = self.redis_cache.pipeline(transaction=False)

            pipe.sadd(redis_key, post_id)
            pipe.expire(redis_key, 10)
            pipe.scard(redis_key)
            result = pipe.execute()

            remain = 10 - result[-1]
            if remain <= 0:
                redis_key = USER_REQUEST_LIMIT + remote_ip
                self.redis_cache.setex(redis_key, 120, '1')
        else:
            return False
        return remain
