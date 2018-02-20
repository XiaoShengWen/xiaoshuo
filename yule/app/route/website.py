# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado.web import url

from yule.app.handler.website import index
from yule.app.handler.website import check
from yule.app.handler.website import verify_code
from yule.app.handler.website import register
from yule.app.handler.website import login
from yule.app.handler.website import admin_user_info
from yule.app.handler.website import user_auth
from yule.app.handler.website import xiaoshuo
from yule.app.handler.website.cms import videos


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

    # 后台功能
    url(r"/cms/video/list", videos.VideoHandler, name='cms_video_list'),

    # 小说列表页面
    url(r"/xiaoshuo", xiaoshuo.ListHandler, name='xiaoshuo_list'),

    # 视频列表页面
    url(r"/video", xiaoshuo.ListHandler, name='video_list'),
]
