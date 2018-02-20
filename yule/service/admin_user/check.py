# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import re
from yule.database.data_factory.admin_user import AdminUserDataFactory
from yule.lib.service import Service

from yule.service.constants.user import LoginConstant


class CheckService(Service):

    def __init__(self):
        super(Service, self).__init__()
        self.__admin_user_data_factory = AdminUserDataFactory()

    def check_account(self, account):
        """
        :param account:
        :return:
        0 用户名可用
        1 用户名最少3个字符
        2 用户名不能包含除英文、数字、下划线、@之外的字符
        3 用户名已存在
        4 用户名为空
        """
        flag = 4
        if account:
            if len(account) < LoginConstant.USER_ACCOUNT_MIN_LENGTH:
                # 用户名最少3个字符
                flag = 1
            else:
                if not re.search(LoginConstant.USER_ACCOUNT_CHAR_ALLOWED, account):
                    # 用户名不能包含除英文、数字、下划线、@之外的字符
                    flag = 2
                else:
                    admin_user = self.__admin_user_data_factory.get_admin_user_by_account(account=account, with_slave=True)
                    if admin_user:
                        # 用户名已存在
                        flag = 3
                    else:
                        # 用户名可用
                        flag = 0

        return flag

    def check_nickname(self, nickname):
        """
        :param nickname:
        :return:
        0 昵称可用
        1 昵称不能以空格开头
        2 昵称为空
        """
        flag = 2
        if nickname:
            if nickname.startswith(' '):
                # 昵称不能以空格开头
                flag = 1
            else:
                flag = 0

        return flag

    def check_password(self, password):
        """
        :param password:
        :return:
        0 密码可用
        1 密码最少6个字符
        2 密码至少同时包含英文字母和数字
        3 密码为空
        """
        flag = 3
        if password:
            if len(password) < LoginConstant.USER_PASSWORD_MIN_LENGTH:
                # 密码最少6个字符
                flag = 1
            else:
                if not re.search(LoginConstant.USER_PASSWORD_CHAR_ALLOWED, password):
                    # 密码至少同时包含英文字母和数字
                    flag = 2
                else:
                    # 密码可用
                    flag = 0

        return flag

    def check_email(self, email):
        """
        :param email:
        :return:
        0 邮箱可用
        1 邮箱不正确
        2 邮箱为空
        """
        flag = 2
        if email:
            if not re.search(LoginConstant.EMAIL_CHAR_ALLOWED, email):
                # 邮箱不正确
                flag = 1
            else:
                # 邮箱可用
                flag = 0

        return flag

    def check_qq(self, qq):
        """
        :param qq:
        :return:
        0 QQ可用
        1 QQ不正确
        2 QQ为空
        """
        flag = 2
        if qq:
            if not re.search(LoginConstant.QQ_CHAR_ALLOWED, qq):
                # QQ不正确
                flag = 1
            else:
                # QQ可用
                flag = 0

        return flag

    def check_mobile(self, mobile):
        """
        :param mobile:
        :return:
        0 手机号可用
        1 手机号不正确
        2 手机号为空
        """
        flag = 2
        if mobile:
            if not re.search(LoginConstant.MOBILE_CHAR_ALLOWED, mobile):
                # 手机号不正确
                flag = 1
            else:
                # 手机号可用
                flag = 0
        else:
            flag = 0

        return flag
