# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import CHAR
from sqlalchemy.types import String
from sqlalchemy.types import TIMESTAMP

from cms.lib.model import BaseModel


class AdminUserModel(BaseModel):
    __tablename__           = 'diyidan_admin_user'
    __table_args__          = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    """
    后台用户    复用第一弹管理后台cms中的diyidan_admin_user
    
    admin_user_id                   ID          INT
    admin_user_account              账户名      string
    admin_user_realname             姓名        string
    admin_user_email                邮箱        string
    admin_user_phone                电话        string
    admin_user_password             PASS        string
    admin_user_salt                 SALT        string
    admin_user_role                 角色        INT
    admin_user_permision_music      音乐权限    INT
    admin_user_permision_tag        标签权限    INT
    admin_user_permision_apply      APPLY       INT
    admin_user_permision_area_rank  AREA_RANK   INT
    admin_user_permision_report     REPORT      INT
    admin_user_permision_chat       CHAT        INT
    admin_user_permision_push       PUSH        INT
    admin_user_permision_user       USER        INT
    admin_user_permision_post       POST        INT
    admin_user_permision_comment    COMMENT     INT
    admin_user_permision_live_stats LIVE_STATS  INT
    admin_user_permision_game       GAME        INT
    admin_user_permision_shop       SHOP        INT
    admin_user_permision_kol        KOL         INT
    admin_user_permision_audit      AUDIT       INT
    admin_user_channel              渠道来源    string
    admin_user_channel_multiple     邀请我的人  string
    admin_user_regtime              注册时间    TIMESTAMP
    admin_user_update_time          更新时间    TIMESTAMP
    """

    admin_user_id                   = Column(BIGINT(20,unsigned=True), primary_key=True)
    admin_user_account              = Column(String(64),nullable=False,unique=True)
    admin_user_realname             = Column(String(64),unique=True)
    admin_user_email                = Column(String(64),unique=True)
    admin_user_phone                = Column(String(64),unique=True)
    admin_user_password             = Column(CHAR(64))
    admin_user_salt                 = Column(CHAR(10))
    admin_user_role                 = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('100') )
    admin_user_permision_music      = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_tag        = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_apply      = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_area_rank  = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_report     = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_chat       = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_push       = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_user       = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_post       = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_comment    = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_live_stats = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_game       = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_shop       = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_kol        = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_permision_audit      = Column(TINYINT(4,unsigned=True),nullable=False, server_default = sqlalchemy.sql.expression.text('0'))
    admin_user_channel              = Column(String(64))
    admin_user_channel_multiple     = Column(INTEGER(10,unsigned=True)) # 邀请我的人
    admin_user_regtime              = Column(TIMESTAMP,server_default = sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))
    admin_user_update_time          = Column(TIMESTAMP,server_default = sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))
