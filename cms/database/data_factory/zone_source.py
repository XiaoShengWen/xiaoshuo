# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import traceback
import logging

from datetime import datetime
from datetime import timedelta
from sqlalchemy.sql.expression import func

from tornado.concurrent import run_on_executor

from cms.lib.mysql import db_with_main_thread
from cms.lib.mysql import db_with_thread_pool
from cms.lib.data_factory import DataFactory
from cms.lib.singleton import singleton

from cms.database.model.zone_source import AdZoneSourceModel


@singleton
class ZoneSourceDataFactory(DataFactory):

    @db_with_main_thread
    def create_zone_source(self, **kwargs):

        account = kwargs.get('account', None)
        nickname = kwargs.get('nickname', None)
        password = kwargs.get('password', None)
        salt = kwargs.get('salt', None)
        email = kwargs.get('email', None)
        mobile = kwargs.get('mobile', None)
        qq = kwargs.get('qq', None)
        fee_mode = kwargs.get('fee_mode', None)
        fee_account_name = kwargs.get('fee_account_name', None)
        fee_account_num = kwargs.get('fee_account_num', None)
        fee_account_deposit = kwargs.get('fee_account_deposit', None)
        note = kwargs.get('note', None)
        source = kwargs.get('source', None)
        manager = kwargs.get('manager', None)

        if not fee_mode:
            fee_mode = u'支付宝'  # 默认支付宝

        # 用户核心表
        zone_source = AdZoneSourceModel()
        zone_source.zone_source_account = account
        zone_source.zone_source_nickname = nickname
        zone_source.zone_source_password = password
        zone_source.zone_source_salt = salt
        zone_source.zone_source_email = email
        zone_source.zone_source_mobile = mobile
        zone_source.zone_source_qq = qq
        zone_source.zone_source_fee_mode = fee_mode
        zone_source.zone_source_fee_account_name = fee_account_name
        zone_source.zone_source_fee_account_num = fee_account_num
        zone_source.zone_source_fee_account_deposit = fee_account_deposit
        zone_source.zone_source_note = note
        zone_source.zone_source_source = source
        zone_source.zone_source_manager = manager

        result = self.save_without_commit(zone_source)
        if result:
            self.do_commit()
            source_id = zone_source.zone_source_id
        else:
            source_id = None

        return source_id

    @db_with_main_thread
    def update_zone_source(self, source_id, **kwargs):
        if not source_id:
            return

        nickname = kwargs.get('nickname', None)
        password = kwargs.get('password', None)
        salt = kwargs.get('salt', None)
        email = kwargs.get('email', None)
        mobile = kwargs.get('mobile', None)
        qq = kwargs.get('qq', None)
        fee_mode = kwargs.get('fee_mode', None)
        fee_account_name = kwargs.get('fee_account_name', None)
        fee_account_num = kwargs.get('fee_account_num', None)
        fee_account_deposit = kwargs.get('fee_account_deposit', None)
        note = kwargs.get('note', None)
        source = kwargs.get('source', None)

        # 用户核心表
        zone_source = self.get_zone_source_by_id(source_id=source_id)
        if not zone_source:
            return

        if nickname:
            zone_source.zone_source_nickname = nickname
        if password:
            zone_source.zone_source_password = password
        if salt:
            zone_source.zone_source_salt = salt
        if email:
            zone_source.zone_source_email = email
        if mobile:
            zone_source.zone_source_mobile = mobile
        if qq:
            zone_source.zone_source_qq = qq
        if fee_mode:
            zone_source.zone_source_fee_mode = fee_mode
        if fee_account_name:
            zone_source.zone_source_fee_account_name = fee_account_name
        if fee_account_num:
            zone_source.zone_source_fee_account_num = fee_account_num
        if fee_account_deposit:
            zone_source.zone_source_fee_account_deposit = fee_account_deposit
        if note:
            zone_source.zone_source_note = note
        if source:
            zone_source.zone_source_source = source

        result = self.save_without_commit(zone_source)
        if result:
            self.do_commit()
            source_id = zone_source.zone_source_id
        else:
            source_id = None

        return source_id

    @db_with_main_thread
    def exist_zone_source(self, account=None, nickname=None, email=None, mobile=None):
        if not any([account, nickname, email, mobile]):
            return  # 有误

        query = self.db_session.query(AdZoneSourceModel.zone_source_id)
        if account:
            query = query.filter(AdZoneSourceModel.zone_source_account == account)
        if account:
            query = query.filter(AdZoneSourceModel.zone_source_nickname == nickname)
        if account:
            query = query.filter(AdZoneSourceModel.zone_source_email == email)
        if account:
            query = query.filter(AdZoneSourceModel.zone_source_mobile == mobile)
        result = query.first()
        if result:
            return 1  # 存在

        return -1  # 不存在

    @db_with_main_thread
    def get_zone_source_by_id(self, source_id, with_slave=False):
        query = self.db_session.query(AdZoneSourceModel).filter(AdZoneSourceModel.zone_source_id == source_id)
        zone_source = self._query_one(query)
        return zone_source

    @db_with_main_thread
    def get_zone_source_by_account(self, account, with_slave=False):
        query = self.db_session.query(AdZoneSourceModel).filter(AdZoneSourceModel.zone_source_account == account)
        zone_source = self._query_one(query)
        return zone_source

    @db_with_main_thread
    def get_zone_source_by_nickname(self, nickname, with_slave=False):
        query = self.db_session.query(AdZoneSourceModel).filter(AdZoneSourceModel.zone_source_nickname == nickname)
        zone_source = self._query_one(query)
        return zone_source
