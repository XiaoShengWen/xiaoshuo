# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.netutil

import yule.app.route.website
import yule.lib.config
import socket
import signal
import logging
import time
import gc
import os

from yule.lib.jinja2_tornado import JinjaLoader
from yule.lib import uimodules
from yule.lib.config import website_config as app_config

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0

tornado.options.define(
    'port',
    default=app_config.get('port'),
    help='run on the given port',
    type=int
)
tornado.options.define(
    'debug',
    default=app_config.get('debug'),
    help="debug mode",
    type=bool
)
tornado.options.define(
    'autoreload',
    default=app_config.get('autoreload'),
    help='autoreload on',
    type=bool
)
tornado.options.define(
    'process',
    default=app_config.get('process'),
    help='process count',
    type=int)


class Global:
    is_in_stop = False


def refresh_memory():
    gc.collect()
    if not Global.is_in_stop:
        now = time.time()
        tornado.ioloop.IOLoop.instance().add_timeout(now + 3, refresh_memory)


def shutdown():
    logging.info('Stopping http server')

    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()
    now = time.time()
    io_loop.add_timeout(now + 15, server.stop)  # 不接收新的 HTTP 请求

    deadline = now + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
    # global Global.is_in_stop
    Global.is_in_stop = True

    def stop_loop():

        now = time.time()
        # logging.warning(io_loop._callbacks)
        # logging.warning(io_loop._timeouts)
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 2, stop_loop)
        else:
            io_loop.stop()  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            logging.info('Shutdown')

    stop_loop()


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(shutdown)


class Application(tornado.web.Application):
    def __init__(self):
        command_setting = dict()
        command_setting['port'] = tornado.options.options.port
        command_setting['debug'] = tornado.options.options.debug
        command_setting['autoreload'] = tornado.options.options.autoreload
        # command_setting['debug'] = True
        command_setting['autoreload'] = True
        command_setting['login_url'] = '/login'
        command_setting['ui_modules'] = uimodules
        command_setting['template_loader'] = JinjaLoader(os.path.join(os.path.dirname(__file__), 'yule/templates/'))
        app_config.update(command_setting)
        settings = app_config

        # huadu.app.route.website.handlers.extend(huadu.app.route.activity.handlers)
        tornado.web.Application.__init__(self, yule.app.route.website.handlers, **settings)


if __name__ == "__main__":

    gc.set_threshold(10000)

    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    if tornado.options.options.process:
        server.bind(tornado.options.options.port, family=socket.AF_INET, reuse_port=True)
        server.start(tornado.options.options.process)
    else:
        sockets = tornado.netutil.bind_sockets(tornado.options.options.port, family=socket.AF_INET)
        server.add_sockets(sockets)

    logging.info("yule server started...")
    tornado.ioloop.IOLoop.instance().start()
