### 实时验证

描述 ：用户输入信息实时验证唯一性

地址 ：/cms/v1/check

请求 ：get

参数：

```
account     (必填):   string (用户名)
callback    (选填):   string (jsonp 回调方法)
```

成功返回值：
```json
{
    "message": "验证通过",
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
