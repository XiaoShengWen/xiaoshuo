# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import CHAR
from sqlalchemy.types import String
from sqlalchemy.types import TIMESTAMP

from yule.lib.model import BaseModel


class AdminUserModel(BaseModel):
    __tablename__ = 'xiaoshuo_admin_user'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    """
    后台用户
    
    admin_user_id                   ID          INT
    admin_user_account              账户名      string
    admin_user_nickname             昵称        string
    admin_user_email                邮箱        string
    admin_user_phone                电话        string
    admin_user_password             PASS       string
    admin_user_salt                 SALT       string
    admin_user_role                 用户角色     INT
    admin_user_create_time          创建时间    TIMESTAMP
    admin_user_update_time          更新时间    TIMESTAMP on update CURRENT_TIMESTAMP()
    """

    admin_user_id                   = Column(BIGINT(20, unsigned=True), primary_key=True)
    admin_user_account              = Column(String(64), nullable=False, unique=True)
    admin_user_nickname             = Column(String(64), unique=True)
    admin_user_email                = Column(String(64), unique=True)
    admin_user_phone                = Column(String(64), unique=True)
    admin_user_password             = Column(CHAR(64))
    admin_user_salt                 = Column(CHAR(10))
    admin_user_role                 = Column(TINYINT(4, unsigned=True), nullable=False, server_default=sqlalchemy.sql.expression.text('100'))
    admin_user_create_time          = Column(TIMESTAMP, server_default=sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))
    admin_user_update_time          = Column(TIMESTAMP, server_default=sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'))
