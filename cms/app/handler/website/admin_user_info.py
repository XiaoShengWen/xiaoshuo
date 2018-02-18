# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

from cms.lib import website
from cms.lib import utils
from cms.lib import system_code
from cms.lib.website import authenticated
from cms.service.users.check import CheckService
from cms.service.admin_user.admin_user import AdminUserService
from cms.service.admin_user.admin_user_info import AdminUserInfoService
from cms.service.other.request import RequestService
from tornado import gen


class AdminUserInfoHandler(website.BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    @authenticated
    @gen.coroutine
    def put(self, *args, **kwargs):
        admin_user_info_service = AdminUserInfoService()
        check_service = CheckService()

        user_id = self.get_body_argument('userId', None)
        nickname = self.get_body_argument('nickname', None)
        email = self.get_body_argument('email', None)
        mobile = self.get_body_argument('mobile', None)

        if user_id:
            user_id = utils.val_to_int(user_id)

        code = 0
        message = ''
        result = {
            'userId': None
        }

        if user_id and user_id == self.current_user:
            if nickname:
                # 昵称检查
                nickname_flag = check_service.check_nickname(nickname)
            else:
                nickname_flag = 0
            if email:
                # 邮箱检查
                email_flag = check_service.check_email(email)
            else:
                email_flag = 0
            if mobile:
                # 手机号检查
                mobile_flag = check_service.check_mobile(mobile)
            else:
                mobile_flag = 0

            if sum([nickname_flag, email_flag, mobile_flag]) == 0:
                # 修改用户信息
                admin_user_id = admin_user_info_service.update_admin_user_info(
                    user_id,
                    nickname,
                    email,
                    mobile,
                )

                if user_id:
                    result['userId'] = admin_user_id
            else:
                # 昵称
                if nickname_flag == 1:
                    code = system_code.USER_NICKNAME_CHAR_NOT_ALLOWED
                # 邮箱
                elif email_flag == 1:
                    code = system_code.USER_EMAIL_DISABLED
                # 手机
                elif mobile_flag == 1:
                    code = system_code.USER_MOBILE_DISABLED
        else:
            code = system_code.USER_IS_DISABLED

        self.render_json(result, code, message)
        return

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        request_service = RequestService()
        admin_user_info_service = AdminUserInfoService()

        user_id = self.get_query_argument('userId', None)

        if user_id:
            user_id = utils.val_to_int(user_id)

        code = 0
        result = dict()

        if user_id:
            if not user_id:
                user_id = self.current_user

            if user_id:
                remain_request = request_service.get_remain_request(self.request.remote_ip, user_id)
                if remain_request < 0:
                    yield gen.sleep(3)
                if remain_request > -5:
                    is_me = (int(user_id) == self.current_user)
                    admin_user, code = admin_user_info_service.get_admin_user(user_id)
                    if admin_user:
                        result['isMe'] = is_me
                        result['user'] = {
                            'userId': user_id,
                            'account': admin_user.get('admin_user').admin_user_account,
                            'nickname': admin_user.get('admin_user').admin_user_realname,
                            'email': admin_user.get('admin_user').admin_user_email,
                            'mobile': admin_user.get('admin_user').admin_user_phone,
                        }
                else:
                    yield gen.sleep(10)
                    code = system_code.SERVER_ERROR
            else:
                code = system_code.PARAM_ERROR
        else:
            code = system_code.PARAM_ERROR

        self.render_json(result, code)
        return

    def options(self, *args, **kwargs):
        self.write('GET,PUT')


class UserPassResetHandler(website.BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    @authenticated
    @gen.coroutine
    def put(self, *args, **kwargs):
        admin_user_service = AdminUserService()
        check_service = CheckService()

        user_id = self.get_body_argument('userId', None)
        password_origin = self.get_body_argument('passwordOrigin', None)
        password = self.get_body_argument('password', None)
        password_confirm = self.get_body_argument('passwordConfirm', None)

        if user_id:
            user_id = utils.val_to_int(user_id)

        code = 0
        message = ''
        result = {
            'userId': None
        }

        if all([user_id, password_origin, password, password_confirm]):

            if admin_user_service.is_user_pass(user_id, password_origin):
                if password == password_confirm:
                    if user_id and user_id == self.current_user:
                        if password:
                            # 密码检查
                            password_flag = check_service.check_password(password)
                        else:
                            password_flag = 0

                        if password_flag == 0:
                            # 修改用户密码
                            user_id = admin_user_service.reset_user_pass(
                                user_id,
                                password,
                            )

                            if user_id:
                                result['userId'] = user_id
                        else:
                            # 密码
                            if password_flag == 1:
                                code = system_code.USER_PWD_TOO_SHORT
                            elif password_flag == 2:
                                code = system_code.USER_PWD_DISABLED

                    else:
                        code = system_code.USER_IS_DISABLED
                else:
                    code = system_code.USER_PWD_CONFIRM_NOT_MATCH
            else:
                code = system_code.USER_PWD_ERROR
        else:
            code = system_code.PARAM_MISS

        self.render_json(result, code, message)
        return

    def get(self, *args, **kwargs):
        pass

    def options(self, *args, **kwargs):
        self.write('PUT')
