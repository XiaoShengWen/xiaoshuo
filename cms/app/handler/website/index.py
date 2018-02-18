# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from cms.lib import system_code

from cms.lib.website import authenticated
from cms.lib.website import BaseWebsiteHandler
from cms.service.users.session import SessionService
from cms.service.admin_user.admin_user import AdminUserService


class IndexHandler(BaseWebsiteHandler):

    def prepare(self):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self.render('index.html')

    def options(self, *args, **kwargs):
        self.write('GET')
