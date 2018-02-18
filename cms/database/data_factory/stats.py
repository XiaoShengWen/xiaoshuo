# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from sqlalchemy import desc

from cms.lib.mysql import db_with_main_thread
from cms.lib.data_factory import DataFactory
from cms.lib.singleton import singleton

from cms.database.model.zone_plan import AdZonePlanModel
from cms.database.model.zone_stats import AdZoneHotStatModel


@singleton
class StatsFactory(DataFactory):

    @db_with_main_thread
    def get_plan_stats(self, plan_id=None, zone_id=None, app_id=None, start_date=None, end_date=None, with_slave=False):
        query = self.db_session.query(AdZoneHotStatModel, AdZonePlanModel)
        if isinstance(plan_id, (list, tuple)):
            query = query.filter(AdZoneHotStatModel.stats_plan_id.in_(plan_id))
        else:
            query = query.filter(AdZoneHotStatModel.stats_plan_id == plan_id)
        query = query.outerjoin(AdZonePlanModel, AdZonePlanModel.az_plan_id == AdZoneHotStatModel.stats_plan_id)
        query = query.order_by(desc(AdZoneHotStatModel.stats_id))
        stats = self._query_all(query)
        return stats

    @db_with_main_thread
    def get_all_plan(self, plan_id=None, start_date=None, end_date=None, with_slave=False):
        query = self.db_session.query(AdZonePlanModel).filter(AdZonePlanModel.az_plan_if_draft == 0)
        if isinstance(plan_id, (list, tuple)):
            query = query.filter(AdZonePlanModel.az_plan_id.in_(plan_id))
        else:
            query = query.filter(AdZonePlanModel.az_plan_id == plan_id)
        if start_date:
            query = query.filter(AdZonePlanModel.az_plan_end_date >= start_date)
        if end_date:
            query = query.filter(AdZonePlanModel.az_plan_start_date <= end_date)
        all_zone = self._query_all(query)
        return all_zone
