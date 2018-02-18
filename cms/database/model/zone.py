# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import String
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import Text
from sqlalchemy.types import Date

from cms.lib.model import BaseModel


class AdZoneModel(BaseModel):
    """空间号"""
    __tablename__ = 'diyidan_ad_zone'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    # ID
    ad_zone_id = Column(BIGINT(20, unsigned=True), primary_key=True)
    # 名称
    ad_zone_name = Column(String(128), nullable=False)  # 要求不超过80个字符
    # 空间号码
    ad_zone_qq = Column(String(32))
    # 空间类型
    ad_zone_type = Column(String(32))
    # 联系人
    ad_zone_contact_person = Column(String(64))
    # 联系方式类型
    ad_zone_contact_type = Column(String(32))
    # 联系方式，可选
    ad_zone_contact_num = Column(String(64))
    # 邮箱
    ad_zone_contact_email = Column(String(64))
    # 结算方式
    ad_zone_fee_mode = Column(String(32))
    # 单价，以分为单位存
    ad_zone_fee_unit = Column(INTEGER(10, unsigned=True))
    # 注册成本，以分为单位存
    ad_zone_reg_fee_unit = Column(INTEGER(10, unsigned=True))
    # 结算账号昵称
    ad_zone_fee_account_name = Column(String(64))
    # 结算账号
    ad_zone_fee_account_num = Column(String(64))
    # 开户行
    ad_zone_fee_account_deposit = Column(String(64))
    # 日均浏览量
    ad_zone_daily_view = Column(INTEGER(10, unsigned=True), nullable=False, default=0)
    # 运营时长
    ad_zone_operation_time = Column(TINYINT(4, unsigned=True), nullable=False, default=0)
    # 接单次数
    ad_zone_order_count = Column(TINYINT(4, unsigned=True), nullable=False, default=0)
    # 名单类型
    ad_zone_list_type = Column(String(32))
    # 广告主
    ad_zone_source_id = Column(BIGINT(20, unsigned=True))
    # 产品
    ad_zone_app_id = Column(BIGINT(20, unsigned=True))
    # 投放类型
    ad_zone_trial_type = Column(String(32))
    # 渠道
    ad_zone_ac_id = Column(BIGINT(20, unsigned=True))
    # 素材链接
    ad_zone_material_url = Column(String(128))
    # 目标链接
    ad_zone_target_url = Column(String(128))
    # 评估结果
    ad_zone_evaluate = Column(String(32))
    # 评估时间
    ad_zone_evaluate_date = Column(Date)
    # 标签
    ad_zone_tag = Column(String(255))
    # 备注
    ad_zone_note = Column(Text)
    # 空间配置id，一对多
    ad_zone_config_ids = Column(String(255))
    # 空间状态，100在用/9已删除
    ad_zone_status = Column(TINYINT(4, unsigned=True), nullable=False, server_default=sqlalchemy.sql.expression.text('100'))
    # 创建时间
    ad_zone_create_time = Column(TIMESTAMP, server_default=sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))
    # 空间添加(管理)者
    ad_zone_manager = Column(BIGINT(20, unsigned=True))
    # 空间所有者
    ad_zone_owner = Column(BIGINT(20, unsigned=True))
