# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

from cms.lib import website
from cms.lib import utils
from cms.lib import system_code
from cms.lib.website import authenticated
from cms.service.other.request import RequestService
from cms.service.admin_user.admin_user_info import AdminUserInfoService
from tornado import gen


class UserAuthHandler(website.BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        request_service = RequestService()
        admin_user_info_service = AdminUserInfoService()

        user_id = self.get_query_argument('userId', None)

        if user_id:
            user_id = utils.val_to_int(user_id)
        else:
            user_id = self.current_user

        result = dict()

        if user_id:
            remain_request = request_service.get_remain_request(self.request.remote_ip, user_id)
            if remain_request < 0:
                yield gen.sleep(3)
            if remain_request > -5:
                is_me = (user_id == self.current_user)
                user, code = admin_user_info_service.get_admin_user(user_id)
                if user:
                    result['isMe'] = is_me
                    result['user'] = {
                        'userId': user_id
                    }
            else:
                yield gen.sleep(10)
                code = system_code.SERVER_ERROR
        else:
            code = system_code.PARAM_ERROR

        self.render_json(result, code)
        return

    def options(self, *args, **kwargs):
        self.write('GET')
