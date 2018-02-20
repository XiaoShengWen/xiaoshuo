# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import os
import redis
import ConfigParser
from yule.lib.singleton import singleton


@singleton
class Redis(object):
    __cf = None
    __redis = None
    __redis_cache = None
    __redis_single = None

    def __init__(self):
        if self.__cf is None:
            environment = os.getenv('HUADU_ENV')
            base_dir = '%s%s%s%s%s' % (os.path.dirname(__file__), os.sep, '..', os.sep, 'conf')

            if environment == 'prod':
                conf_file = 'redis.conf'
            else:
                conf_file = 'redis_dev.conf'

            self.__cf = ConfigParser.ConfigParser()
            self.__cf.read(os.path.join(base_dir, conf_file))

    def get_redis(self):
        """
        主要业务的数据 有过期时间
        :return:
        """
        if self.__redis is None:
            config = dict(self.__cf.items('redis'))
            self.__redis = redis.StrictRedis(host=config.get('redis_host'))

        return self.__redis

    def get_redis_cache(self):
        """
        缓存数据 和 消息队列
        :return:
        """

        if self.__redis_cache is None:
            config = dict(self.__cf.items('redis_cache'))
            if config.get('redis_db'):
                self.__redis_cache = redis.StrictRedis(
                    host=config.get('redis_host'),
                    db=int(config.get('redis_db'))
                )
            else:
                self.__redis_cache = redis.StrictRedis(host=config.get('redis_host'))

        return self.__redis_cache

    def get_redis_single(self):
        """
        session 数据
        :return:
        """
        if self.__redis_single is None:
            config = dict(self.__cf.items('redis_single'))
            self.__redis_single = redis.StrictRedis(host=config.get('redis_host'))

        return self.__redis_single
