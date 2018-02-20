# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import tornado.web
import ujson as json
import functools

from tornado.web import HTTPError
from yule.service.users.session import SessionService
from yule.service.admin_user.admin_user_info import AdminUserInfoService
from yule.lib import system_code
from yule.lib.utils import val_to_int

IMAGE_BASE_URL = ''


def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            # raise HTTPError(403)
            self.write(json.dumps({'data': None, 'code': system_code.USER_IS_NOT_LOGIN, 'message': '未登录'}, ensure_ascii=False))
            return
        return method(self, *args, **kwargs)

    return wrapper


class BaseWebsiteHandler(tornado.web.RequestHandler):
    # session_id
    __session_id = None
    __device_id = None
    __user_info_service = None
    __session_service = None

    def initialize(self):
        self.__admin_user_info_service = AdminUserInfoService()
        self.__session_service = SessionService()

        self.__set_session()
        self.__set_header()

    def __set_header(self):
        ALLOW_ORIGIN = [
            'http://127.0.0.1:3000',  # me
            'http://192.168.2.97:3000',  # me
            'http://192.168.2.97'  # nginx
        ]
        self.set_header('Access-Control-Allow-Methods', 'POST, PUT, GET, OPTIONS, DELETE')
        origin = self.request.headers.get('Origin')
        if origin in ALLOW_ORIGIN:
            self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header(
            'Access-Control-Allow-Headers',
            'Origin, X-Requested-With, Content-Type, Accept, client_id, uuid, Authorization'
        )
        # self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Content-Type', 'text/html; charset="utf-8"')
        self.set_header('Server', 'HuaduServer')
        self.set_header('Cache-Control', 'private')
        self.set_header('Version', 'v1.0')

    def __set_session(self):
        """
        初始化session
        :return:
        """
        self.__session_id = self.get_secure_cookie('session_id')

        if not self.__session_id:
            self.__session_id = self.__session_service.generage_session_id()
            self.set_secure_cookie('session_id', self.__session_id, expires_days=None, httponly=True)

    @property
    def session_id(self):
        if self.__session_id is None:
            self.__set_session()
        return self.__session_id

    @property
    def device_id(self):
        if self.__device_id is None:
            self.__device_id = self.request.headers.get('deviceId', None)
        return self.__device_id

    def render_json(self, data=None, code=0, message=''):
        if message == '':
            message = system_code.MSG.get(code, system_code.MSG.get(system_code.SERVER_ERROR))
        result = {
            'data': data if data else None,
            'code': code,
            'message': message
        }
        self.write(json.dumps(result, ensure_ascii=False))

    def render_jsonp(self, callback, data=None, code=0, message=''):
        if message == '':
            message = system_code.MSG.get(code, system_code.MSG.get(system_code.SERVER_ERROR))
        result = {
            'data': data if data else None,
            'code': code,
            'message': message
        }

        result = '%s(%s)' % (str(callback), json.dumps(result, ensure_ascii=False))
        self.write(result)

    def get_current_user(self):
        user_id = self.__session_service.get_session(self.session_id, 'user_id')
        token = self.get_secure_cookie("token_id")
        user_id = self.__admin_user_info_service.get_current_user(
            self.session_id,
            user_id,
            token
        )
        if user_id:
            return user_id
        else:
            return None

    def render(self, template_name, **kwargs):

        request_time = ''
        if self.request.request_time():
            request_time = self.request.request_time() * 1000
            request_time = int(request_time)
            request_time = str(request_time) + 'ms'

        if self.current_user:
            super(BaseWebsiteHandler, self).render(
                    template_name,
                    admin_user_id=self.current_user,
                    request_time=request_time,
                    xsrf_form_html=self.xsrf_form_html,
                    int=val_to_int,
                    reverse_url=self.reverse_url,
                    static_url=self.static_url,
                    image_base_url=IMAGE_BASE_URL,
                    **kwargs
            )
        else:
            super(BaseWebsiteHandler, self).render(
                    template_name,
                    request_time=request_time,
                    image_base_url=IMAGE_BASE_URL,
                    int=val_to_int,
                    reverse_url=self.reverse_url,
                    xsrf_form_html=self.xsrf_form_html,
                    static_url=self.static_url,
                    **kwargs
            )

