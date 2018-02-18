# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from cms.lib import system_code

from cms.lib.website import BaseWebsiteHandler
from cms.service.users.check import CheckService


class CheckHandler(BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    @gen.coroutine
    def get(self, *args, **kwargs):
        check_service = CheckService()

        account = self.get_query_argument('account', None)
        callback = self.get_query_argument('callback', None)

        code = 0
        message = ''
        result = dict()

        if not any([account]):
            code = system_code.PARAM_MISS
        else:
            if account:
                # 用户名检查
                account_flag = check_service.check_account(account)
            else:
                account_flag = 0

            if sum([account_flag]) == 0:
                code = system_code.SUCCESS
            else:
                # 用户名
                if account_flag == 1:
                    code = system_code.USER_ACCOUNT_TOO_SHORT
                elif account_flag == 2:
                    code = system_code.USER_ACCOUNT_CHAR_NOT_ALLOWED
                elif account_flag == 3:
                    code = system_code.USER_IS_EXIST

        if callback:
            self.render_jsonp(callback, result, code, message)
        else:
            self.render_json(result, code, message)
        return

    def options(self, *args, **kwargs):
        self.write('GET')
