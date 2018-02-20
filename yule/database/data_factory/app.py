# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from sqlalchemy.sql.expression import distinct

from yule.lib.mysql import db_with_main_thread
from yule.lib.data_factory import DataFactory
from yule.lib.singleton import singleton

from yule.database.model.app import AdAppModel


@singleton
class AppDataFactory(DataFactory):

    @db_with_main_thread
    def get_app_by_id(self, app_id, with_slave=False):
        query = self.db_session.query(AdAppModel)
        query = query.filter(AdAppModel.app_id == app_id)
        zone = self._query_one(query)
        return zone

    @db_with_main_thread
    def get_all_app(self, app_id, with_slave=False):
        query = self.db_session.query(AdAppModel)
        if isinstance(app_id, (list, tuple)):
            query = query.filter(AdAppModel.app_id.in_(app_id))
        else:
            query = query.filter(AdAppModel.app_id == app_id)
        all_zone = self._query_all(query)
        if all_zone:
            return all_zone

        return []
