# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

from cms.lib.diyidan_redis import Redis


class Service(object):
    __redis_instance = None

    __redis = None
    __redis_cache = None
    __redis_single = None

    def __init__(self):
        pass

    def __get_redis(self):
        """
        获取redis实例
        :return:
        """
        if self.__redis_instance is None:
            self.__redis_instance = Redis()

        return self.__redis_instance

    @property
    def redis(self):
        """
        主要业务的数据 有过期时间
        :return:
        """
        if self.__redis is None:
            self.__redis = self.__get_redis().get_redis()
        return self.__redis

    @property
    def redis_cache(self):
        """
        缓存数据 和 消息队列
        :return:
        """
        if self.__redis_cache is None:
            self.__redis_cache = self.__get_redis().get_redis_cache()
        return self.__redis_cache

    @property
    def redis_single(self):
        """
        db_session 数据
        :return:
        """
        if self.__redis_single is None:
            self.__redis_single = self.__get_redis().get_redis_single()
        return self.__redis_single
