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
        callback    (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "userId": 35
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
## **注册/登录/退出：**

* 用户接口：
    * 描述：注册
    * 地址：/api/v1/register
    * 请求：POST
    * 参数：
        ```
        account     (必填):   string     (用户名)
        password    (必填):   string     (密码)
        ```
    * 返回值：
        ```json
        {
            "message": "操作成功",
            "code": 0,
            "data": {
                "token": "bqxigwej8czy3fo7n9vrt4ds025makuh",
                "userId": 35
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "操作成功",
            "code": 0,
            "data": {
                "token":  "用户token",
                "userId": "用户id"
            }
        }
        ```

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
                "userId": 35
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
## **数据统计页面**

* 拉取user登录头部信息
    * 描述：获取用户登录后头部信息
    * 地址：/api/v1/userInfoShort
    * 请求：GET
    * 参数：
        ```
        userId      (必填):   int     (用户ID)
        callback    (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "qq": "122211221",
                    "nickname": "xxaxaa",
                    "account": "huadu",
                    "userId": 35,
                    "avatar": "https://image.diyidan.net/post/2017/11/19/bWeT79y7vwR4GETq.jpg"
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
                    "qq": "用户QQ",
                    "nickname": "用户昵称",
                    "account": "用户账号",
                    "userId": "用户ID",
                    "avatar": "用户头像"
                },
                "isMe": true
            }
        }
        ```


* 获取数据统计信息
    * 描述 ：获取用户空间号的数据统计信息
    * 地址 ：/api/v1/planStats
    * 请求 ：get
    * 参数 ：
        ```
        userId       (必填):   int     (用户ID)
        zoneId       (必填):   int     (空间ID)
        appId        (选填):   int     (产品ID)
        page         (选填):   int     (当前页数)
        callback     (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "list": [
                    {
                        "planName": "1.1-第一弹-安卓美化",
                        "planStart": 1514764800,
                        "planEnd": 1514851200,
                        "appId": 2,
                        "planId": 368,
                        "rate": 0,
                        "rank": 16,
                        "zoneId": 100002
                    },
                    {
                        "planName": "12.22-第一弹-家政妇",
                        "planStart": 1513900800,
                        "planEnd": 1513987200,
                        "appId": 2,
                        "planId": 361,
                        "rate": 0,
                        "rank": 7,
                        "zoneId": 100002
                    },
                    {
                        "planName": "12.22-第一弹-家政妇",
                        "planStart": 1513900800,
                        "planEnd": 1513987200,
                        "appId": 2,
                        "planId": 361,
                        "rate": 0,
                        "rank": 9,
                        "zoneId": 100002
                    }
                ],
                "top": {
                    "planName": "1.1-第一弹-安卓美化",
                    "planStart": 1514764800,
                    "planEnd": 1514851200,
                    "appId": 2,
                    "planId": 368,
                    "rate": 0,
                    "rank": 16,
                    "zoneId": 100002
                },
                "userId": 35,
                "pageInfo": {
                    "total": 3,
                    "page": 1
                }
            }
        }
        ```
    * 失败示例(无数据) ：
        ```json
        {
            "message": "没有数据",
            "code": 107000,
            "data": {
                "userId": 35
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "list": [
                    {
                    "planName": "计划名称",
                    "planStart": "计划开始日期",
                    "planEnd": "计划结束日期",
                    "appId": "产品ID",
                    "planId": "计划ID",
                    "rate": "评分",
                    "rank": "排名",
                    "zoneId": "空间ID"
                }
                ],
                "top": {
                    "planName": "计划名称",
                    "planStart": "计划开始日期",
                    "planEnd": "计划结束日期",
                    "appId": "产品ID",
                    "planId": "计划ID",
                    "rate": "评分",
                    "rank": "排名",
                    "zoneId": "空间ID"
                },
                "userId": "用户ID",
                "pageInfo": {
                    "total": "总数",
                    "page": "当前页数"
                }
            }
        }
        ```

* 获取搜索栏数据
    * 描述 ：获取搜索栏的相关数据
    * 地址 ：/api/v1/searchBar
    * 请求 ：get
    * 参数 ：
        ```
        userId       (必填):   int     (用户ID)
        type         (必填):   int     (搜索类型)
        zoneId       (必填):   int     (空间ID)
        planId       (选填):   int     (计划ID)
        appId        (选填):   int     (产品ID)
        ```
    * 说明 ：
        - 搜索栏为空间号，则?type=zone, 可获取搜索栏列表，
        若需要单个的空间号信息，则?type=zone&zoneId=123,
        - 搜索栏为空间计划，则?type=plan, 可获取空间计划列表，
        若需要与空间号联动，则?type=plan&zoneId=123, 可获取空间号123相关的计划列表,
        若需要单个的计划信息，则?type=plan&planId=123,
        - 搜索栏为产品，则?type=app, 可获取产品列表，
        若需要与空间号联动，则?type=app&zoneId=123, 可获取空间号123相关的产品列表,
        若需要单个的产品信息，则?type=app&appId=123,
    * 返回值 ：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "data": [
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号1",
                        "zoneId": 100001
                    },
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号2",
                        "zoneId": 100002
                    },
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号3",
                        "zoneId": 100003
                    },
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号4",
                        "zoneId": 100004
                    },
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号5",
                        "zoneId": 100005
                    },
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号6",
                        "zoneId": 100006
                    },
                    {
                        "zoneQQ": "1",
                        "zoneName": "测试号7",
                        "zoneId": 100007
                    }
                ],
                "type": "zone"
            }
        }
        ```
    * 失败示例(无数据) ：
        ```json
        {
            "message": "缺少参数",
            "code": 100002,
            "data": {
                "type": ""
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 200,
            "data": {
                "data": [
                    {
                        "zoneQQ": "空间QQ",
                        "zoneName": "空间名称",
                        "zoneId": "空间ID"
                    }
                ],
                "type": "搜索类型"
            }
        }
        ```

---
## **排行榜页面**

* 搜索栏（选择计划）
    * 描述：选择计划下拉框
    * 地址：
    * 请求：
    * 参数：

* 排行榜
    * 描述： 排行榜信息
    * 地址：
    * 请求：
    * 参数：

---
## **广告素材页**

* 广告素材包列表
    * 描述：素材包首页列表
    * 地址：/api/v1/material/
    * 请求： GET
    * 参数：
        ```
        userId       (必填):   int     (用户ID)
        callback    (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": [{
                "planId": "12",
                "appName": "产品",
                "materialId": "13"
            }]
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": [{
                "planId": "计划ID",
                "appName": "产品名称",
                "materialId": "素材ID"
            }]
        }
        ```

* 广告素材详情
    * 描述：素材详情
    * 地址：/api/v1/material/material_detail/
    * 请求：GET
    * 参数：
        ```
        userId           (必填):   int     (用户ID)
        materialId       (必填):   int     (素材ID)
        callback         (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": [{
                "planId": "12",
                "appName": "产品",
                "materialId": "13",
                "materialDocuments": "这是文案，可能会很长",
                "materialImgUrls": "http://huadu.png"
            }]
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": [{
                "planId": "计划ID",
                "appName": "产品名称",
                "materialId": "素材ID",
                "materialDocuments": "素材文案",
                "materialImgUrls": "素材图片"
            }]
        }
        ```

---
## **我的空间页**

* 空间列表
    * 描述：我的空间号列表
    * 地址：/api/v1/zoneList
    * 请求：GET
    * 参数：
        ```
        userId      (必填):   int     (用户ID)
        callback    (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": [
                {
                    "orderCount": 0,
                    "operationTime": 0,
                    "zoneId": 100468,
                    "zoneQQ": "55747491",
                    "dailyView": 25,
                    "zoneType": "綜合",
                    "zoneName": "掏心话"
                },
                {
                    "orderCount": 0,
                    "operationTime": 0,
                    "zoneId": 100469,
                    "zoneQQ": "20905665",
                    "dailyView": 25,
                    "zoneType": "綜合",
                    "zoneName": "中高考学术墙"
                }
            ]
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 200,
            "data": [
                {
                    "orderCount": "接单次数",
                    "operationTime": "运营时间",
                    "zoneId": "空间ID",
                    "zoneQQ": "空间QQ",
                    "dailyView": "空间浏览量",
                    "zoneType": "空间类型",
                    "zoneName": "空间名称"
                }
            ]
        }
        ```

* 编辑空间号（编辑按钮）
    * 描述：点击编辑后编辑空间号
    * 地址：/api/v1/zone
    * 请求：PUT
    * 参数：
        ```
        userId               (必填):   int       (用户ID)
        zoneId               (必填):   int       (空间ID)
        zoneName             (必填):   string    (空间名称)
        zoneType             (必填):   string    (空间类型)
        dailyView            (必填):   int       (空间浏览量)
        operationTime        (必填):   int       (运营时间)
        orderCount           (必填):   int       (订单次数)
        callback             (选填):   string    (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "zoneId": 100470
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "zoneId": "空间ID"
            }
        }
        ```

* 删除空间号
    * 描述：删除空间
    * 地址：/api/v1/zone
    * 请求：DELETE
    * 参数：
        ```
        userId               (必填):   int       (用户ID)
        zoneId               (必填):   int       (空间ID)
        callback             (选填):   string    (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "zoneId": 100471
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "zoneId": "被删除的空间ID"
            }
        }
        ```

* 添加空间号
    * 描述：添加空间号
    * 地址：/api/v1/zone
    * 请求：POST
    * 参数：
        ```
        userId               (必填):   int       (用户ID)
        zoneName             (必填):   string    (空间名称)
        zoneQQ               (必填):   string    (空间QQ)
        zoneType             (必填):   string    (空间类型)
        dailyView            (必填):   int       (空间浏览量)
        operationTime        (必填):   int       (运营时间)
        orderCount           (必填):   int       (订单次数)
        callback             (选填):   string    (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 200,
            "data": {
                "zoneId": 100470
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "空间已存在",
            "code": 103001,
            "data": {
                "zoneId": null
            }
        }
        ```


*  获取空间基本信息
    * 描述 ：获取某个空间基本信息
    * 地址 ：/api/v1/zone
    * 请求 ：get
    * 参数 ：
        ```
        userId               (必填):   int       (用户ID)
        zoneId               (必填):   string    (空间ID)
        callback             (选填):   string    (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "orderCount": 0,
                "operationTime": 0,
                "zoneId": 100468,
                "zoneQQ": "55747491",
                "dailyView": 25,
                "zoneType": "久合",
                "zoneName": "掏心话"
            }
        }
        ```
    * 失败返回：
        ```json
        {
            "message": "空间不存在",
            "code": 103000,
            "data": {
                "zoneId": "100"
            }
        }
        ```
    * 返回值字段含义：
        ```json
        {
            "message": "success",
            "code": 200,
            "data": {
                    "orderCount": "接单次数",
                    "operationTime": "运营时间",
                    "zoneId": "空间ID",
                    "zoneQQ": "空间QQ",
                    "dailyView": "空间浏览量",
                    "zoneType": "空间类型",
                    "zoneName": "空间名称"
                }
        }
        ```

---
## **账号设置页面**

* 拉取账号信息
    * 描述：拉取用户账号信息
    * 地址：/api/v1/userInfo
    * 请求：GET
    * 参数：
        ```
        userId      (必填):   int     (用户ID)
        callback    (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "user": {
                    "qq": "122211221",
                    "account": "huadu",
                    "feeAccountNum": "1zhifubao-name1",
                    "mobile": "13212341234",
                    "nickname": "xxaxaa",
                    "feeAccountName": "1zhifubao1",
                    "userId": 35,
                    "email": "123@qq.com"
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
                    "qq": "账号QQ",
                    "account": "账户名",
                    "feeAccountNum": "账户支付宝账号",
                    "mobile": "账户手机号",
                    "nickname": "账户昵称",
                    "feeAccountName": "账户支付宝账号名",
                    "userId": "账户ID",
                    "email": "账户邮箱"
                },
                "isMe": true
            }
        }
        ```

* 修改信息
    * 描述：修改账号信息
    * 地址: /api/v1/userInfo
    * 请求：PUT
    * 参数：
        ```
        userId               (必填):   int     (用户ID)
        nickname             (必填):   string  (用户昵称)
        qq                   (必填):   string  (用户QQ)
        mobile               (必填):   string  (用户手机号)
        feeAccountName       (必填):   string  (用户支付宝名称)
        feeAccountNum        (必填):   string  (用户支付宝账号)
        callback             (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": 35
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
        callback             (选填):   string  (jsonp 回调方法)
        ```
    * 返回值：
        ```json
        {
            "message": "success",
            "code": 0,
            "data": {
                "userId": 35
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
