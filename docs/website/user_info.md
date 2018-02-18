### 获取用户信息

描述 ：通过用户ID获取用户详情

地址 ：/cms/v1/userInfo

请求 ：get

参数：

```
userId       (必填):   int     (用户ID)
callback    (选填):   string  (jsonp 回调方法)
```

返回值：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "user": {
            "qq": "12312321",
            "account": "huadu",
            "feeAccountNum": "zhifubao-name1",
            "mobile": "12345678901",
            "nickname": "haudu1",
            "feeAccountName": "zhifubao1",
            "userId": 35,
            "email": "123@qq.com"
        },
        "isMe": true
    }
}
```


返回值字段含义：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "user": {
            "qq": "账号QQ",
            "email": "账户邮箱",
            "feeAccountName": "账户支付宝账号名",
            "feeAccountNum": "账户支付宝账号",
            "account": "账户名",
            "userId": "账户ID",
            "nickname": "账户昵称",
            "mobile": "账户手机号"
        },
        "isMe": true
    }
}
```

### 修改用户信息

描述 ：修改账号基本信息

地址 ：/cms/v1/userInfo

请求 ：put

参数：

```
userId               (必填):   int     (用户ID)
nickname             (选填):   string  (用户昵称)
qq                   (选填):   string  (用户QQ)
mobile               (选填):   string  (用户手机号)
feeAccountName       (选填):   string  (用户支付宝名称)
feeAccountNum        (选填):   string  (用户支付宝账号)
callback             (选填):   string  (jsonp 回调方法)
```

返回值：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "userId": 35
    }
}
```


返回值字段含义：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "userId": "用户ID"
    }
}
```

### 修改用户密码

描述 ：修改账号密码

地址 ：/cms/v1/passReset

请求 ：put

参数：

```
userId               (必填):   int     (用户ID)
passwordOrigin       (选填):   string  (用户原始密码)
password             (选填):   string  (用户新密码)
passwordConfirm      (选填):   string  (用户确认新密码)
callback             (选填):   string  (jsonp 回调方法)
```

返回值：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "userId": 35
    }
}
```


返回值字段含义：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "userId": "用户ID"
    }
}
```

