### 用户登录接口

描述 ：用户使用平台账号密码登录

地址 ：/cms/v1/login

请求 ：post

参数：

```
account    (必填):   string (用户手机号)
password    (必填):   string (用户密码)
callback    (选填):   string (jsonp 回调方法)
```

成功返回值：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": null
}
```

失败返回值：
```json
{
    "message": "缺少参数",
    "code": 0,
    "data": null
}
```


### 用户退出接口

描述 ：用户退出平台账号

地址 ：/cms/v1/login

请求 ：delete

参数：

```
callback    (选填):   string (jsonp 回调方法)
```

返回值：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": null
}
```