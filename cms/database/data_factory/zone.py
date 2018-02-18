# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from sqlalchemy.sql.expression import distinct

from cms.lib.mysql import db_with_main_thread
from cms.lib.data_factory import DataFactory
from cms.lib.singleton import singleton

from cms.database.model.zone import AdZoneModel


@singleton
class ZoneDataFactory(DataFactory):

    @db_with_main_thread
    def add_zone(self, **kwargs):

        zone_name = kwargs.get('zone_name', None)
        zone_qq = kwargs.get('zone_qq', None)
        zone_type = kwargs.get('zone_type', None)
        daily_view = kwargs.get('daily_view', None)
        operation_time = kwargs.get('operation_time', None)
        order_count = kwargs.get('order_count', None)
        zone_owner = kwargs.get('zone_owner', None)

        # 空间核心表
        zone = AdZoneModel()
        zone.ad_zone_name = zone_name
        zone.ad_zone_qq = zone_qq
        zone.ad_zone_type = zone_type
        zone.ad_zone_daily_view = daily_view
        zone.ad_zone_operation_time = operation_time
        zone.ad_zone_order_count = order_count
        zone.ad_zone_owner = zone_owner

        result = self.save(zone)
        if result:
            zone_id = zone.ad_zone_id
        else:
            zone_id = None

        return zone_id

    @db_with_main_thread
    def update_zone(self, zone_id, **kwargs):
        if not zone_id:
            return

        zone_name = kwargs.get('zone_name', None)
        zone_type = kwargs.get('zone_type', None)
        daily_view = kwargs.get('daily_view', None)
        operation_time = kwargs.get('operation_time', None)
        order_count = kwargs.get('order_count', None)

        # 空间核心表
        zone = self.get_zone_by_id(zone_id=zone_id, reuse_session=True)
        if not zone:
            return

        if zone_name:
            zone.ad_zone_name = zone_name
        if zone_type:
            zone.ad_zone_type = zone_type
        if daily_view:
            zone.ad_zone_daily_view = daily_view
        if operation_time:
            zone.ad_zone_operation_time = operation_time
        if order_count:
            zone.ad_zone_order_count = order_count

        result = self.save_without_commit(zone)
        if result:
            self.do_commit()
            zone_id = zone.ad_zone_id
        else:
            zone_id = None

        return zone_id

    @db_with_main_thread
    def update_zone_status(self, zone_id, zone_status):
        if not zone_id:
            return

        # 空间核心表
        zone = self.get_zone_by_id(zone_id=zone_id)
        if not zone:
            return

        zone.ad_zone_status = zone_status

        result = self.save_without_commit(zone)
        if result:
            self.do_commit()
            zone_id = zone.ad_zone_id
        else:
            zone_id = None

        return zone_id

    @db_with_main_thread
    def exist_zone(self, zone_name=None, zone_qq=None):
        if not any([zone_name, zone_qq]):
            return  # 有误

        query = self.db_session.query(AdZoneModel.ad_zone_id)
        if zone_name:
            query = query.filter(AdZoneModel.ad_zone_name == zone_name)
        if zone_qq:
            query = query.filter(AdZoneModel.ad_zone_qq == zone_qq)
        result = self._query_first(query)
        if result:
            return 1  # 存在

        return -1  # 不存在

    @db_with_main_thread
    def get_zone_by_id(self, zone_id, with_slave=False):
        query = self.db_session.query(AdZoneModel).filter(AdZoneModel.ad_zone_status == 100)
        query = query.filter(AdZoneModel.ad_zone_id == zone_id)
        zone = self._query_one(query)
        return zone

    @db_with_main_thread
    def get_zone_by_source(self, source_id, with_slave=False):
        query = self.db_session.query(AdZoneModel).filter(AdZoneModel.ad_zone_status == 100)
        query = query.filter(AdZoneModel.ad_zone_owner == source_id)
        all_zone = self._query_all(query)
        return all_zone
