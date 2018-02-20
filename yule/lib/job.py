# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import time
from abc import abstractmethod


class Job(object):
    # 执行1次
    sig_terminate = 1
    # 执行多次
    sig_continue = 2
    # 超时设置
    timeout = 60
    reload_interval = 3600
    # 最大执行数量
    max_exec_count = 1000

    def run(self):
        start = time.time()
        count = 0
        self.loop_start()

        while True:
            data = self.retrieve_data()

            step = self.consume(data)

            count += 1

            if self.sig_terminate == step:
                break

            if self.reload_interval and start + self.reload_interval < time.time():
                break

            if count == self.max_exec_count:
                break

        self.loop_end()

    @abstractmethod
    def retrieve_data(self):
        pass

    @abstractmethod
    def consume(self, data):
        pass

    def loop_start(self):
        pass

    def loop_end(self):
        pass
