# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from sqlalchemy.sql.expression import func

from yule.lib.mysql import db_with_main_thread

from yule.lib.singleton import singleton
from yule.lib.data_factory import DataFactory


@singleton
class UuidDataFactory(DataFactory):
    @db_with_main_thread
    def get_short_uuid(self, with_slave = False):
        uuid = self.db_session.execute('select UUID_SHORT()').fetchone()[0]
        uuid = int(uuid)
        uuid &= 0xffffffffffffff
        uuid += 87 << 56
        # if uuid < 6269010681299730432:
        #     uuid += 4899916394579099648
        return uuid

    @db_with_main_thread
    def get_very_short_uuid(self, with_slave = False):
        uuid = self.db_session.execute('select UUID_SHORT()').fetchone()[0]
        uuid = int(uuid)
        uuid &= 0xffffffffffffff
        return uuid

    def shrink_short_uuid(self, uuid):
        uuid = int(uuid)
        uuid &= 0xffffffffffffff
        return uuid

    def restore_short_uuid(self, uuid):
        uuid = int(uuid)
        uuid &= 0xffffffffffffff
        uuid += 87 << 56
        return uuid
