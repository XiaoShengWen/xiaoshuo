# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import logging
import traceback
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound


class DataFactory(object):
    db_session = None
    scope_db_session = None

    def __init__(self):
        pass

    def save_without_commit(self, obj):
        try:
            self.db_session.add(obj)
            self.db_session.flush()
            return True
        except Exception as e:
            logging.warning(traceback.format_exc())
            self.db_session.rollback()
            return False

    def do_commit(self):
        try:
            self.db_session.commit()
            return True
        except Exception as e:
            logging.warning(traceback.format_exc())
            self.db_session.rollback()
            return False

    def save(self, obj):
        try:
            self.db_session.add(obj)
            self.db_session.commit()
            return True
        except IntegrityError, e:
            self.db_session.rollback()
            logging.warning('Item exists.')
            logging.warning('obj = ' + str(obj))
            return False
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.db_session.rollback()
            return False

    def do_scope_commit(self):
        try:
            self.scope_db_session.commit()
            return True
        except Exception as e:
            logging.warning(traceback.format_exc())
            self.scope_db_session.rollback()
            return False

    def set_query_page(self, query, page, page_size):
        if not page_size:
            page_size = 15
        page_size = int(page_size)

        if page_size:
            query = query.limit(page_size)

        if not page:
            page = 1

        page = 1 if int(page) < 1 else int(page)

        ##数据库中从0开始，但是页面里从1开始，所以要减一
        page = page - 1

        if page:
            query = query.offset(page * page_size)

        return query

    def _query_one(self, query):
        try:
            obj = query.one()
            return obj
        except MultipleResultsFound, e:
            # logging.warning(str(query))
            return None
        except NoResultFound, e:
            # logging.warning(str(query))
            return None
        except Exception, e:
            logging.warning(traceback.format_exc())
            return None

    def _query_all(self, query):
        try:
            obj = query.all()

            return obj
        except NoResultFound, e:
            # logging.warning(str(query))
            return None
        except Exception, e:
            logging.warning(traceback.format_exc())
            return None

    def _query_first(self, query):
        try:
            obj = query.first()

            return obj
        except NoResultFound, e:
            # logging.warning(str(query))
            return None
        except Exception,e:
            logging.warning(traceback.format_exc())
            return None
