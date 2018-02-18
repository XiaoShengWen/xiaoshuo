# # 花度派单系统页面api

---
[TOC]

---
## **所有页面：**

* 用户接口：
    * 描述：通过用户ID获取用户信息
    * 地址：/api/v1/userId
    * 请求：GET
    * 参数：
        ```
        userId      (选填):   int     (登录操作后返回的userId)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "userId": 10
                },
                "isMe": true
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "userId": "用户ID"
                },
                "isMe": true
            }
        }
        ```

---
## **登录/退出：**

* 用户接口：
    * 描述：登录
    * 地址：/api/v1/login
    * 请求：POST
    * 参数：
        ```
        account     (必填):   string     (用户名)
        password    (必填):   string     (密码)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": 10
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": "用户ID"
            }
        }
        ```

* 用户接口：
    * 描述：退出
    * 地址：/api/v1/login
    * 请求：DELETE
    * 参数：
        ```
        null
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": null
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": null
        }
        ```

---
## **账号设置页面**

* 拉取账号信息
    * 描述：拉取用户账号信息
    * 地址：/api/v1/adminUserInfo
    * 请求：GET
    * 参数：
        ```
        userId      (必填):   int     (用户ID)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "mobile": "18616757463",
                    "nickname": "super_admin",
                    "account": "diyidan_super_admin",
                    "userId": 10,
                    "email": "admin_super@diyidan.com"
                },
                "isMe": true
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "mobile": "手机号",
                    "nickname": "姓名",
                    "account": "账户名",
                    "userId": "用户ID",
                    "email": "邮箱"
                },
                "isMe": true
            }
        }
        ```

* 修改信息
    * 描述：修改账号信息
    * 地址: /api/v1/adminUserInfo
    * 请求：PUT
    * 参数：
        ```
        userId               (必填):   int     (用户ID)
        nickname             (必填):   string  (用户昵称)
        email                (必填):   string  (用户邮箱)
        mobile               (必填):   string  (用户手机号)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": 10
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": "用户ID"
            }
        }
        ```

* 修改密码
    * 描述：修改账号密码
    * 地址：/api/v1/passReset
    * 请求：PUT
    * 参数：
        ```
        userId               (必填):   int     (用户ID)
        passwordOrigin       (必填):   string  (用户原始密码)
        password             (必填):   string  (用户新密码)
        passwordConfirm      (必填):   string  (用户确认新密码)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": 10
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": "用户ID"
            }
        }
        ```
