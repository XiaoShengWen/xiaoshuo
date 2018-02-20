# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from yule.lib.mysql import db_with_main_thread
from yule.lib.data_factory import DataFactory
from yule.lib.singleton import singleton

from yule.database.model.admin_user import AdminUserModel


@singleton
class AdminUserDataFactory(DataFactory):

    @db_with_main_thread
    def update_admin_user(self, admin_user_id, **kwargs):
        if not admin_user_id:
            return

        nickname = kwargs.get('nickname', None)
        password = kwargs.get('password', None)
        salt = kwargs.get('salt', None)
        email = kwargs.get('email', None)
        mobile = kwargs.get('mobile', None)

        # 用户核心表
        admin_user = self.get_admin_user_by_id(admin_user_id=admin_user_id)
        if not admin_user:
            return

        if nickname:
            admin_user.admin_user_nickname = nickname
        if password:
            admin_user.admin_user_password = password
        if salt:
            admin_user.admin_user_salt = salt
        if email:
            admin_user.admin_user_email = email
        if mobile:
            admin_user.admin_user_phone = mobile

        result = self.save_without_commit(admin_user)
        if result:
            self.do_commit()
            user_id = admin_user.admin_user_id
        else:
            user_id = None

        return user_id

    @db_with_main_thread
    def exist_admin_user(self, account=None, nickname=None, email=None, mobile=None):
        if not any([account, nickname, email, mobile]):
            return  # 有误

        query = self.db_session.query(AdminUserModel.admin_user_id)
        if account:
            query = query.filter(AdminUserModel.admin_user_account == account)
        if account:
            query = query.filter(AdminUserModel.admin_user_nickname == nickname)
        if account:
            query = query.filter(AdminUserModel.admin_user_email == email)
        if account:
            query = query.filter(AdminUserModel.admin_user_phone == mobile)
        result = query.first()
        if result:
            return 1  # 存在

        return -1  # 不存在

    @db_with_main_thread
    def get_admin_user_by_id(self, admin_user_id, with_slave=False):
        query = self.db_session.query(AdminUserModel).filter(AdminUserModel.admin_user_id == admin_user_id)
        admin_user = self._query_one(query)
        return admin_user

    @db_with_main_thread
    def get_admin_user_by_account(self, account, with_slave=False):
        query = self.db_session.query(AdminUserModel).filter(AdminUserModel.admin_user_account == account)
        admin_user = self._query_one(query)
        return admin_user
