# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.types import String
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import Text
from sqlalchemy.types import Date

from yule.lib.model import BaseModel


class AdAppModel(BaseModel):
    __tablename__       = 'diyidan_ad_app'
    __table_args__      = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    # ID
    app_id = Column(BIGINT(20,unsigned=True), primary_key=True)
    # 广告主
    app_source_id = Column(INTEGER(10, unsigned = True))
    # 产品名称
    app_name = Column(String(32))
    # 广告主
    app_source_name = Column(String(32))
    # 产品类型
    app_type = Column(String(32))
    # 下载链接
    app_download_url = Column(String(128))
    # MD5
    app_md5 = Column(String(32))
    # 版本
    app_version_name = Column(String(32))
    # 包名
    app_package_name = Column(String(32))
    #
    app_version_code = Column(INTEGER(10, unsigned = True))
    #
    app_size = Column(INTEGER(10, unsigned = True))
    # 投放开始日期
    app_date_start = Column(Date)
    # 投放结束日期
    app_date_end = Column(Date)
    # 计费周期
    app_fee_cycle = Column(String(32))
    # 计费方式
    app_fee_mode = Column(String(4))
    # 成本
    app_fee_unit = Column(INTEGER(10, unsigned = True))
    # 备注
    app_note = Column(Text)
    # 渠道数量
    app_channel_num = Column(INTEGER(10, unsigned = True))
    # 创建时间
    app_create_time = Column(TIMESTAMP,server_default = sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))
    # 管理者
    app_manager = Column(BIGINT(20,unsigned=True))