# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from yule.lib import system_code
from yule.lib import utils

from yule.lib.website import authenticated
from yule.lib.website import BaseWebsiteHandler
from yule.service.users.session import SessionService
from yule.service.admin_user.admin_user import AdminUserService


class ListHandler(BaseWebsiteHandler):

    def prepare(self):
        pass

    @gen.coroutine
    def post(self, *args, **kwargs):
        admin_user_service = AdminUserService()

        account = self.get_body_argument('account', None)
        password = self.get_body_argument('password', None)
        remember = self.get_body_argument('remember', None)

        code = 0
        message = ''
        result = {
            'userId': None
        }

        if not all([account, password]):
            code = system_code.PARAM_MISS
        else:
            admin_user, code = admin_user_service.login(account, password)

            if code == 0:
                code = system_code.SUCCESS
                # 登录设置token
                token = admin_user_service.create_user_token(admin_user.admin_user_id, 'website')
                if token:
                    self.set_secure_cookie('token_id', token)
                session_service = SessionService()
                session_service.set_session(self.session_id, 'user_id', admin_user.admin_user_id)
                result['userId'] = admin_user.admin_user_id

                self.redirect('/index')
                return
            else:
                code = system_code.USER_LOGIN_ERROR

        self.render_json(result, code, message)
        return

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        categories = utils.get_url_content('http://novel.juhe.im/categories')
        print categories.get('data')
        self.render('video/list.html')

    def options(self, *args, **kwargs):
        self.write('POST,DELETE')
