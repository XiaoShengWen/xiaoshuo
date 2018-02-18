# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import pycurl
import logging
import ujson as json
import tornado.httpclient
from tornado import gen


@gen.coroutine
def send_http_request(url, method="GET", headers=None, body=None, no_delay=True, is_json=True, **kwargs):
    http_client = tornado.httpclient.AsyncHTTPClient(max_clients=125)
    prepare_curl_no_delay = None
    support_method = ['GET', 'POST', 'PUT', 'DELETE']
    # 默认方法
    if method not in support_method:
        method = 'GET'

    # 默认包头
    if not headers:
        headers = {
            "Content-Type": 'application/x-www-form-urlencoded',
        }

    if no_delay:
        prepare_curl_no_delay = lambda x: x.setopt(pycurl.TCP_NODELAY, 1)

    data = None
    try:
        request = tornado.httpclient.HTTPRequest(
            url,
            method=method,
            headers=headers,
            body=body,
            prepare_curl_callback=prepare_curl_no_delay,
            allow_ipv6=False,
            **kwargs
        )

        response = yield http_client.fetch(request)
        if response and response.code == 200:
            data = response.body

    except tornado.httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        logging.warning("Error: " + str(e))
        logging.warning("url: " + url)

    except Exception as e:
        # Other errors are possible, such as IOError.
        logging.warning("Error: " + str(e))

    finally:
        if is_json:
            data = json.loads(data)
        raise gen.Return(data)
