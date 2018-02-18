# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import os
import ConfigParser
import functools
import logging
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine

# 主库 master
engine_master = None
# 从库
engine_slave = None

session_master = None
session_slave = None
session_thread_pool = None

environment = os.getenv('HUADU_ENV')
base_dir = '%s%s%s%s%s' % (os.path.dirname(__file__), os.sep, '..', os.sep, 'conf')

if environment == 'prod':
    conf_file = 'mysql.conf'
else:
    conf_file = 'mysql_dev.conf'

cf = ConfigParser.ConfigParser()
cf.read(os.path.join(base_dir, conf_file))

if engine_master is None:
    config = dict(cf.items('mysql'))
    engine_master = create_engine(
        'mysql://%s:%s@%s:%d/%s?charset=utf8' % (
            config.get('mysql_user'),
            config.get('mysql_pass'),
            config.get('mysql_host'),
            3306,
            config.get('mysql_db')
        ),
        encoding='utf8',
        echo=False,
        pool_recycle=10800
    )

if engine_slave is None:
    config = dict(cf.items('mysql_slave'))
    engine_slave = create_engine(
        'mysql://%s:%s@%s:%d/%s?charset=utf8&connect_timeout=10' % (
            config.get('mysql_user'),
            config.get('mysql_pass'),
            config.get('mysql_host'),
            3306,
            config.get('mysql_db')
        ),
        encoding='utf8',
        echo=False,
        pool_recycle=10800
    )

if session_master is None:
    session_master = sessionmaker(bind=engine_master)

if session_slave is None:
    session_slave = sessionmaker(bind=engine_slave, autocommit=True)

if session_thread_pool is None:
    session_thread_pool = scoped_session(sessionmaker(bind=engine_master))


def db_with_main_thread(method):
    """
        该装饰器实现对数据库层方法method调用时的db_session的管理，并达到以下目标：
        1.自动管理method使用的db_session的初始化和释放工作
        2.支持数据库层方法嵌套调用(使用reuse_session标记);

        限制
            当reuse_session为True时，忽略其他控制参数，导致如下限制：
                (1).db_session为主库时，method的一切操作也只能是当前主库;
                (2).db_session为从库时，method的一切操作也只能是当前从库;
                即使用reuse_session时要求所有的操作都在该session上;

            reuse_session设计时最主要考虑两个原则:
            (1).外部调用和内部实现简单;
            (2).一次数据库操作只应该初始化一次数据库session, 就算在write操作嵌套有read操作，
                也不建议分别建立一个master和slave session进行数据库访问;

        NOTE:
            1.注意该装饰器的使用范围，如果在数据库操作中嵌套调用该装饰器装饰过的函数，最好根据业务情况拆分，避免嵌套调用;
            2.该装饰器最初的意图在于实现db_session的及时释放，即一次数据库操作完成后立即释放，而不是等到HTTP请求返回后再释放;
            3.若wrapper中的参数self为单例，则db_with_main_thread装饰过的函数不能支持异步调用，即yield, yield from, gen.coroutine, await等方式

    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        reuse_session = kwargs.get('reuse_session', False)

        if reuse_session:
            # 当使用reuse_session时，则不进行session释放行为
            # 交由嵌套调用的method进行管理
            try:
                return method(self, *args, **kwargs)

            except Exception as ex:
                logging.info(traceback.format_exc())

        else:
            with_slave = kwargs.get('with_slave', False)
            if with_slave:
                self.db_session = session_slave()

            else:
                self.db_session = session_master()

            try:
                return method(self, *args, **kwargs)

            except Exception as ex:
                logging.info(traceback.format_exc())

            finally:
                self.db_session.expunge_all()
                self.db_session.close()

    return wrapper


def db_with_thread_pool(method):
    """
    异步线程
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.scope_db_session = session_thread_pool()
        try:
            return method(self, *args, **kwargs)
        finally:
            session_thread_pool.remove()

    return wrapper
