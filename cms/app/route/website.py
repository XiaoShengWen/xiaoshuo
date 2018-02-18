# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado.web import url

from cms.app.handler.website import index
from cms.app.handler.website import check
from cms.app.handler.website import verify_code
from cms.app.handler.website import register
from cms.app.handler.website import login
from cms.app.handler.website import admin_user_info
from cms.app.handler.website import user_auth


handlers = [
    # 主页和导航页
    url(r"/", index.IndexHandler, name='home'),
    url(r"/index", index.IndexHandler, name='index'),

    # 账号/昵称实时验证
    url(r"/check", check.CheckHandler, name='check'),

    # 验证码
    url(r"/verifyCode", verify_code.VerifyCodeHandler, name='verify_code'),
    # 用户注册
    url(r"/register", register.RegisterHandler, name='register'),

    # 用户登录
    url(r"/login", login.LoginHandler, name='login'),
    # 获取用户信息
    url(r"/adminUserInfo", admin_user_info.AdminUserInfoHandler, name='admin_user_info'),
    # 修改密码
    url(r"/passReset", admin_user_info.UserPassResetHandler, name='pass_reset'),

    # 登录时预先获取用户ID
    url(r"/userId", user_auth.UserAuthHandler, name='user_auth'),
]
