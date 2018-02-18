# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


# 正常可用
USER_STATUS_NORMAL = 100
# 未认证
USER_STATUS_DISABLED = 99
# 已删除
USER_STATUS_DELETED = 9

# 用户创建类型
# 未知
USER_SOURCE_UNKNOWN = 0
# 系统添加
USER_SOURCE_SYSTEM = 1
# 用户注册
USER_SOURCE_REGISTE = 2

# 默认结算方式
USER_DEFAULT_FEE_MODE = u'支付宝'

# 用户自主注册的管理员默认为0
USER_REGISTE_DEFAULT_MANAGER = 0

USER_INFO_STATUS_REDIS_KEY = 'user_status'

# 用户头像
USER_AVATAR_LIST = [
    'http://img.dydab.com/qqzone/11.png',
    'http://img.dydab.com/qqzone/22.png',
    'http://img.dydab.com/qqzone/33.png',
    'http://img.dydab.com/qqzone/44.png',
    'http://img.dydab.com/qqzone/55.png',
    'http://img.dydab.com/qqzone/66.png',
    'http://img.dydab.com/qqzone/77.png',
]


class LoginConstant():

    # 用户名至少要3个字符
    USER_ACCOUNT_MIN_LENGTH = 3
    # 用户名只允许英文+数字+下划线+.+@
    USER_ACCOUNT_CHAR_ALLOWED = u'^[_.@a-zA-Z0-9]+$'

    USER_ACCOUNT_MSG_DICT = {
        'USER_ACCOUNT_MIN_LENGTH': u'用户名至少要3个字符',
        'USER_ACCOUNT_CHAR_ALLOWED': u'用户名不能包含除英文、数字、下划线、@之外的字符',
        'USER_ACCOUNT_EXIST': u'用户名已存在',
    }

    USER_NICKNAME_MSG_DICT = {
        'USER_NICKNAME_NOT_NULL': u'昵称不能为空',
        'USER_ACCOUNT_NOT_STARTSWITH_NULL': u'昵称不能以空格开头',
    }

    # 密码至少要6个字符
    USER_PASSWORD_MIN_LENGTH = 6
    # 密码至少同时英文+数字
    USER_PASSWORD_CHAR_ALLOWED = u'^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]{6,20})$'

    USER_PASSWORD_MSG_DICT = {
        'USER_PASSWORD_MIN_LENGTH': u'密码至少要六位数',
        'USER_PASSWORD_CHAR_ALLOWED': u'密码至少同时包含英文字母和数字',
        'USER_PASSWORD_CONFIRM_WRONG': u'确认密码与密码不匹配',
    }

    # qq
    QQ_CHAR_ALLOWED = u'[1-9][0-9]{4,14}'

    # 手机号
    MOBILE_CHAR_ALLOWED = u'^1[0-9]{10}$'

    # 邮箱
    EMAIL_CHAR_ALLOWED = u'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'
