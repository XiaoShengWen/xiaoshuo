# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import re
import logging
import traceback
import copy
import ujson as json
from yule.lib import utils
from yule.database.data_factory.zone_source import ZoneSourceDataFactory
from yule.lib.service import Service
from yule.lib.singleton import singleton

from yule.service.constants.user import LoginConstant

try:
    # myre = re.compile(ur'[\U00010000-\U0010ffff\u202A-\u202E\u0200-\u0fff]')
    virname_re = re.compile(ur'[\u0200-\u0fff\u202A-\u202E\u0600-\u06ff\u0300-\u0370]')
except re.error:
    # UCS-2 build
    virname_re = re.compile(ur'[\u0200-\u0fff\u202A-\u202E\u0600-\u06ff]')


@singleton
class CheckService(Service):
    __user_data_factory = None

    def __init__(self):
        super(Service, self).__init__()
        self.__user_data_factory = ZoneSourceDataFactory()

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
                    zone_source = self.__user_data_factory.get_zone_source_by_account(account=account, with_slave=True)
                    if zone_source:
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
        # 2 密码至少同时包含英文字母和数字
        3 密码为空
        """
        flag = 3
        if password:
            if len(password) < LoginConstant.USER_PASSWORD_MIN_LENGTH:
                # 密码最少6个字符
                flag = 1
            else:
                flag = 0
                # if not re.search(LoginConstant.USER_PASSWORD_CHAR_ALLOWED, password):
                #     # 密码至少同时包含英文字母和数字
                #     flag = 2
                # else:
                #     # 密码可用
                #     flag = 0

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

    def check_nickname_default(self, nickname):
        """
        :param nickname:
        :return:
        0 成功
        1 存在违规关键字
        2 昵称长度超出限制长度
        3 用户名存在
        4 用户名为空
        """
        flag = 4
        if nickname:
            nickname = nickname.replace('\n', '')
            nickname = nickname.replace('\r', '')
            nickname = nickname.replace('\t', '')
            nickname = nickname.replace(' ', '')

            try:
                nickname = virname_re.sub('', nickname)
                nickname = nickname.strip()
            except Exception as e:
                logging.warning(traceback.format_exc())

            if not self.check_disallowed_words_in_nickname(nickname):
                if len(nickname) <= USER_MAX_ALLOWED_NICKNAME_LENGTH:
                    user_info = self.__user_data_factory.get_user_info_by_nickname(nickname)
                    if user_info:
                        if len(nickname) <= 12:
                            flag = 0
                            nickname += utils.my_random_string(3)
                        else:
                            # 用户名存在
                            flag = 3
                    else:
                        flag = 0
                else:
                    # 用户长度超限
                    flag = 2
            else:
                # 用户昵称存在违规关键字
                flag = 1

        return flag, nickname
