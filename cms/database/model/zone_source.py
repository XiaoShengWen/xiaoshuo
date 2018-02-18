# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import CHAR
from sqlalchemy.types import String
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import Text

from cms.lib.model import BaseModel


class AdZoneSourceModel(BaseModel):
    """空间主"""
    __tablename__ = 'diyidan_ad_zone_source'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    # ID
    zone_source_id = Column(BIGINT(20, unsigned=True), autoincrement=True, primary_key=True)
    # 账户，设计要求不超过24个字符
    zone_source_account = Column(String(128), nullable=False, unique=True)
    # 昵称，要求不超过80个字符
    zone_source_nickname = Column(String(128), nullable=False)
    # 密码
    zone_source_password = Column(CHAR(64), nullable=False)
    # 密码salt
    zone_source_salt = Column(CHAR(10), nullable=False)
    # 邮箱
    zone_source_email = Column(String(64), unique=True)
    # 手机
    zone_source_mobile = Column(String(64))
    # 联系qq
    zone_source_qq = Column(String(64))
    # 联系人
    # zone_source_contact_person  = Column(String(64))
    # 额外联系类型
    zone_source_contact_type = Column(String(32))
    # 额外联系方式
    zone_source_contact_num = Column(String(32))
    # 结算方式，默认支付宝
    zone_source_fee_mode = Column(String(32))
    # 结算账号名称
    zone_source_fee_account_name = Column(String(64))
    # 结算账号
    zone_source_fee_account_num = Column(String(64))
    # 开户行
    zone_source_fee_account_deposit = Column(String(64))
    # 支付宝名称
    # zone_source_fee_alipay_name = Column(String(64))
    # 支付宝账号
    # zone_source_fee_alipay_account = Column(String(64))
    # 备注
    zone_source_note = Column(Text)
    # 账号来源 0未知/1系统/2用户
    zone_source_source = Column(TINYINT(4, unsigned=True), nullable=False, server_default=sqlalchemy.sql.expression.text('0'))
    # 账号状态 100已认证在用/9已删除/99未认证
    zone_source_status = Column(TINYINT(4, unsigned=True), nullable=False, server_default=sqlalchemy.sql.expression.text('100'))
    # 创建时间
    zone_source_create_time = Column(TIMESTAMP,server_default=sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))
    # 更新时间
    zone_source_update_time = Column(TIMESTAMP,server_default=sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'))
    # 空间主添加(管理)者
    zone_source_manager = Column(BIGINT(20,unsigned=True))
