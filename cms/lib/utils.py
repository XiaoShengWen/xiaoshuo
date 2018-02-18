# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from datetime import timedelta
from datetime import datetime
from datetime import date
import ujson as json
import traceback
import logging
import string
import random
import lz4


def my_random_string(string_length=10):
    """using cryptographic safety random functions"""
    ##TODO compare default random & system_random
    # system_random = random.SystemRandom()
    if string_length < 36:
        return ''.join(random.sample(string.ascii_lowercase + string.digits, string_length))

    return ''.join([random.choice(string.ascii_lowercase + string.digits) for x in range(string_length)])


def compare_digest(x, y):
    y = str(y)
    x = str(x)
    if not (isinstance(x, str) and isinstance(y, str)):
        raise TypeError("both inputs should be instances of str")
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= (a != b)

    return result == 0


def zlib_compress(self, content):
    if not content:
        return None
    # 使用lz4 代替
    return lz4.block.compress(content)


def encode_multipart_formdata(self, fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_7d33a816d302b6$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        filename = filename.encode("utf8")
        L.append('--' + BOUNDARY)
        L.append(
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                key, filename
            )
        )
        L.append('Content-Type: %s' % self.get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def lz4_json_encode(json_obj, ensure_ascii=True):
    if not json_obj:
        return None

    try:
        json_str = json.dumps(json_obj, ensure_ascii=ensure_ascii)
        # logging.warning(len(json_str))
        if not json_str:
            return None
        # logging.warning(len(zlib.compress(json_str)))

        result = lz4.block.compress(json_str)
        # logging.warning(len(result))
        return result
    except Exception as e:
        logging.warning(traceback.format_exc())
        return None


def get_todays_weeknum_str():
    today = date.today()
    d = date(2014, 12, 30)
    weeknum = (today - d).days / 7
    return str(weeknum)


def val_to_int(orig_val, d=0, min_val=None, max_val=None):
    result = 0
    try:
        result = int(orig_val)
    except Exception as e:
        result = d

    if min_val:
        result = max(result, min_val)

    if max_val:
        result = min(result, max_val)

    return result


def get_time_str(post_time, post_alt_time=None, with_time_revised=True):
    if not isinstance(post_time, datetime):
        return
    now = datetime.now()
    delta = (now - post_time).total_seconds()
    if with_time_revised:
        delta = delta ** 0.95 if delta > 0 else 0
        post_time = now - timedelta(seconds=delta)
    if post_alt_time and post_alt_time > post_time:
        post_time = post_alt_time

    if delta < 120:
        return u'刚刚'
    elif delta < 3600:
        minutes = delta // 60
        return str(int(minutes) if minutes > 0 else 1) + u'分钟前'
    elif delta < 3600 * 24:
        hours = delta // 3600
        return str(int(hours) if hours > 0 else 1) + u'小时前'
    elif delta < 3600 * 24 * 7:
        in30days = delta // (3600 * 24)
        return str(int(in30days) if in30days > 0 else 1) + u'天前'
    return post_time.strftime("%m-%d")

def get_today_str():
    return str(datetime.now().date())

def get_format_date(date):
    try:
        result = datetime.strftime(date, '%Y-%m-%d')
    except:
        result = ''
    return result
