# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import traceback
import logging
import time
import ujson as json
from yule.lib import utils
from yule.lib.service import Service
from yule.lib.singleton import singleton
from yule.database.redis_key.redis_cache.state import GLOBAL_UNIVERSAL_MSG_QUEUE_LIST
from yule.database.redis_key.redis_cache.state import USER_ONLINE_ITEMS_REDIS_KEY_PRIFEX
from yule.database.redis_key.redis_single.state import USER_LIVE_WEEK_REDIS_KEY_PRIFEX
from yule.database.data_factory.stats import StatsDataFactory
from yule.service.constants.user import USER_RETURN_ACTION


@singleton
class StateService(Service):
    __stats_data_factory = None

    def __init__(self):
        super(Service, self).__init__()
        self.__stats_data_factory = StatsDataFactory()

    def add_universal_msg_to_queue(self, action_master_id, action_type, obj_id, timestamp, priority=False):
        universal_msg_queue_key = GLOBAL_UNIVERSAL_MSG_QUEUE_LIST
        msg_item = {
            "action_master_id": action_master_id,
            "action_type": action_type,
            "obj_id": obj_id,
            "timestamp": int(timestamp),
        }

        msg_enocode_str = utils.lz4_json_encode(msg_item)

        if not msg_enocode_str:
            return False
        if priority:
            result = self.redis_cache.lpush(universal_msg_queue_key, msg_enocode_str)
        else:
            result = self.redis_cache.rpush(universal_msg_queue_key, msg_enocode_str)

        return result

    def increase_user_live_count(self, user_id, date_str):
        try:
            if self.__stats_data_factory.increase_user_live_count(user_id, date_str) == 0:
                self.__stats_data_factory.create_today_stats(date_str)

            redis_key = USER_LIVE_WEEK_REDIS_KEY_PRIFEX
            result = self.redis_single.sadd(redis_key, user_id)
            if result:
                timestamp = int(time.time())
                self.add_universal_msg_to_queue(
                    user_id,
                    USER_RETURN_ACTION,
                    user_id,
                    timestamp,
                    priority=True
                )
            return True
        except Exception as e:
            logging.warning(traceback.format_exc())
            return False

    def increase_user_open_count(self, date_str, user_id, user_ip):
        try:
            item = {
                'online_user_id': user_id,
                'online_user_ip': user_ip,
                'online_date': date_str,
            }
            self.redis_cache.rpush(USER_ONLINE_ITEMS_REDIS_KEY_PRIFEX, json.dumps(item))

            return True
        except Exception as e:
            logging.warning(traceback.format_exc())
            return None
