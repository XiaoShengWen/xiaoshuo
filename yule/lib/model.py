# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import json
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = datetime.strftime(obj, "%Y-%m-%dT%H:%M:%SGMT+08:00")
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object


class MetaModel(object):
    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def to_dict(self):
        return self.columnitems

    def to_json(self):
        return json.dumps(self.to_dict(), cls=DateTimeEncoder)


BaseModel = declarative_base(cls=MetaModel)
