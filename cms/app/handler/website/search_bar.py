# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from cms.lib import utils
from cms.lib import system_code

from cms.lib.website import authenticated
from cms.lib.website import BaseWebsiteHandler
from cms.service.zone.zone import ZoneService
from cms.service.app.app import AppService


class SearchBarHandler(BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    @authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        zone_service = ZoneService()
        app_service = AppService()

        user_id = self.get_query_argument('userId', None)
        select_type = self.get_query_argument('type', None)
        select_zone = self.get_query_argument('zoneId', None)
        select_plan = self.get_query_argument('planId', None)
        select_app = self.get_query_argument('appId', None)

        if user_id:
            user_id = utils.val_to_int(user_id)
        if select_zone:
            select_zone = utils.val_to_int(select_zone)
        if select_plan:
            select_plan = utils.val_to_int(select_plan)
        if select_app:
            select_app = utils.val_to_int(select_app)

        code = 0
        message = ''
        result = {
            'type': select_type
        }
        if not all([user_id, select_type]):
            code = system_code.PARAM_MISS
        elif user_id != self.current_user:
            code = system_code.USER_IS_NOT_ALLOWED
        else:
            data = None
            if data:
                code = system_code.SUCCESS
                result['data'] = data
            else:
                code = system_code.DATA_NOT_FOUND

        self.render_json(result, code, message)
        return

    def options(self, *args, **kwargs):
        self.write('GET')
