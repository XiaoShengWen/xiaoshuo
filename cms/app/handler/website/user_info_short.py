# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import random

from cms.lib import website
from cms.lib import utils
from cms.lib import system_code
from cms.lib.website import authenticated
from cms.service.constants.user import USER_AVATAR_LIST
from cms.service.zone.zone import ZoneService
from cms.service.users.user_info import UserInfoService
from cms.service.other.request import RequestService
from cms.service.users.session import SessionService
from tornado import gen


class UserInfoShortHandler(website.BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    @website.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        request_service = RequestService()
        user_info_service = UserInfoService()
        zone_service = ZoneService()

        user_id = self.get_query_argument('userId', None)
        callback = self.get_body_argument('callback', None)

        if user_id:
            user_id = utils.val_to_int(user_id)

        result = dict()
        if user_id:
            if not user_id:
                user_id = self.current_user

            if user_id:
                remain_request = request_service.get_remain_request(self.request.remote_ip, user_id)
                if remain_request < 0:
                    yield gen.sleep(3)
                if remain_request > -5:
                    is_me = (user_id == self.current_user)
                    user, code = user_info_service.get_user(user_id)
                    zone, code = zone_service.get_owned_zone_ids(user_id)
                    if user:
                        session_service = SessionService()
                        avatar = session_service.get_session(self.session_id, 'avatar')
                        if not avatar:
                            avatar = random.choice(USER_AVATAR_LIST)
                            session_service.set_session(self.session_id, 'avatar', avatar)
                        result['isMe'] = is_me
                        result['user'] = {
                            'userId': user_id,
                            'account': user.get('user').zone_source_account,
                            'nickname': user.get('user').zone_source_nickname,
                            'qq': user.get('user').zone_source_qq,
                            'avatar': avatar
                        }
                else:
                    yield gen.sleep(10)
                    code = system_code.SERVER_ERROR
            else:
                code = system_code.PARAM_ERROR
        else:
            code = system_code.PARAM_ERROR

        if callback:
            self.render_jsonp(callback, result, code)
        else:
            self.render_json(result, code)
        return

    def options(self, *args, **kwargs):
        self.write('GET')
