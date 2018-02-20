# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from yule.lib import system_code

from yule.lib.website import BaseWebsiteHandler
from yule.service.users.user import UserService
from yule.service.users.check import CheckService
from yule.service.users.session import SessionService


class RegisterHandler(BaseWebsiteHandler):

    def prepare(self):
        pass

    @gen.coroutine
    def post(self, *args, **kwargs):
        check_service = CheckService()
        session_service = SessionService()
        user_service = UserService()

        account = self.get_body_argument('account', None)
        password = self.get_body_argument('password', None)
        password_confirm = self.get_body_argument('passwordConfirm', None)
        nickname = self.get_body_argument('nickname', None)
        email = self.get_body_argument('email', None)
        qq = self.get_body_argument('qq', None)
        mobile = self.get_body_argument('mobile', None)
        fee_account_name = self.get_body_argument('feeAccountName', None)
        fee_account_num = self.get_body_argument('feeAccountNum', None)
        callback = self.get_body_argument('callback', None)

        code = 0
        message = ''
        result = {
            'token': None,
            'userId': None
        }

        if not all([account, password, password_confirm, nickname, email, qq, fee_account_name, fee_account_num]):
            code = system_code.PARAM_MISS

        elif password != password_confirm:
            code = system_code.USER_PWD_CONFIRM_NOT_MATCH
        else:
            # 用户名检查
            account_flag = check_service.check_account(account)
            # 昵称检查
            nickname_flag = check_service.check_nickname(nickname)
            # 密码检查
            password_flag = check_service.check_password(password)
            # 邮箱检查
            email_flag = check_service.check_email(email)
            # QQ检查
            qq_flag = check_service.check_qq(qq)
            # 手机号检查
            mobile_flag = check_service.check_mobile(mobile)

            if sum([account_flag, nickname_flag, password_flag, email_flag, qq_flag, mobile_flag]) == 0:
                # 创建用户
                user_id, token = user_service.create_user(
                    account,
                    password,
                    nickname,
                    email,
                    qq,
                    mobile,
                    fee_account_name,
                    fee_account_num
                )

                if user_id and token:
                    self.set_secure_cookie('token_id', token, expires_days=365)
                    session_service.set_session(self.session_id, 'user_id', user_id)
                    result['userId'] = user_id
                    result['token'] = token
                    code = system_code.SUCCESS
            else:
                # 用户名
                if account_flag == 1:
                    code = system_code.USER_ACCOUNT_TOO_SHORT
                elif account_flag == 2:
                    code = system_code.USER_ACCOUNT_CHAR_NOT_ALLOWED
                elif account_flag == 3:
                    code = system_code.USER_IS_EXIST
                # 昵称
                elif nickname_flag == 1:
                    code = system_code.USER_NICKNAME_CHAR_NOT_ALLOWED
                # 密码
                elif password_flag == 1:
                    code = system_code.USER_PWD_TOO_SHORT
                elif password_flag == 2:
                    code = system_code.USER_PWD_DISABLED
                # 邮箱
                elif email_flag == 1:
                    code = system_code.USER_EMAIL_DISABLED
                # QQ
                elif qq_flag == 1:
                    code = system_code.USER_QQ_DISABLED
                # 手机
                elif mobile_flag == 1:
                    code = system_code.USER_MOBILE_DISABLED

        if callback:
            self.render_jsonp(callback, result, code, message)
        else:
            self.render_json(result, code, message)
        return

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self.render('login.html')

    def options(self, *args, **kwargs):
        self.write('POST')
