# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

from diyidan.lib.job import Job
from diyidan.service.users.user import UserService


class DemoJob(Job):
    def __init__(self):
        self.max_exec_count = 2

    def retrieve_data(self):
        """
        设置数据
        :return:
        """
        return UserService().get_user_by_phone('15600615802')

    def consume(self, data):
        """
        脚本逻辑
        :param data:
        :return:
        """
        print data.user_account
        return self.sig_continue

    def loop_end(self):
        """
        脚本结束执行
        :return:
        """
        print 'end'

    def loop_start(self):
        """
        脚本开始之前执行
        :return:
        """
        print 'start'
