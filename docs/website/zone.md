### 获取空间列表

描述 ：获取用户拥有的的空间的列表

地址 ：/cms/v1/zoneList

请求 ：get

参数 ：

```
userId      (必填):   int     (用户ID)
callback    (选填):   string  (jsonp 回调方法)
```

返回值：
```json
{
    "message": "success",
    "code": 200,
    "data": [
        {
            "zoneOrderCount": 0,
            "zoneOperationTime": 0,
            "zoneId": 100468,
            "zoneQQ": "55747491",
            "zoneView": 25,
            "zoneType": "綜合",
            "zoneName": "掏心话"
        },
        {
            "zoneOrderCount": 0,
            "zoneOperationTime": 0,
            "zoneId": 100469,
            "zoneQQ": "20905665",
            "zoneView": 25,
            "zoneType": "綜合",
            "zoneName": "中高考学术墙"
        }
    ]
}
```


返回值字段含义：
```json
{
    "message": "success",
    "code": 200,
    "data": [
        {
            "zoneOrderCount": "接单次数",
            "zoneOperationTime": "运营时间",
            "zoneId": "空间ID",
            "zoneQQ": "空间QQ",
            "zoneView": "空间浏览量",
            "zoneType": "空间类型",
            "zoneName": "空间名称"
        }
    ]
}
```

### 添加空间

描述 ：新增某个空间号

地址 ：/cms/v1/zone

请求 ：post

参数 ：

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

返回值：
```json
{
    "message": "success",
    "code": 200,
    "data": {
        "zoneId": 100470
    }
}
```
失败返回：
```json
{
    "message": "空间已存在",
    "code": 103001,
    "data": {
        "zoneId": null
    }
}
```


### 删除空间

描述 ：删除某个空间号

地址 ：/cms/v1/zone

请求 ：delete

参数 ：

```
userId               (必填):   int       (用户ID)
zoneId               (必填):   int       (空间ID)
callback             (选填):   string    (jsonp 回调方法)
```

返回值：
```json
{
    "message": "success",
    "code": 200,
    "data": {
        "zoneId": 100471
    }
}
```


返回值字段含义：
```json
{
    "message": "success",
    "code": 200,
    "data": {
        "zoneId": "被删除的空间ID"
    }
}
```


### 修改空间

描述 ：修改某个空间号基本信息

地址 ：/cms/v1/zone

请求 ：put

参数 ：

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

返回值：
```json
{
    "message": "success",
    "code": 200,
    "data": {
        "zoneId": 100470
    }
}
```


返回值字段含义：
```json
{
    "message": "success",
    "code": 200,
    "data": {
        "zoneId": "空间ID"
    }
}
```


### 获取空间基本信息

描述 ：获取某个空间基本信息

地址 ：/cms/v1/zone

请求 ：get

参数 ：

```
userId               (必填):   int       (用户ID)
zoneId               (必填):   string    (空间ID)
callback             (选填):   string    (jsonp 回调方法)
```

返回值：
```json
{
    "message": "success",
    "code": 200,
    "data": {
        "zoneOrderCount": 0,
        "zoneOperationTime": 0,
        "zoneId": 100468,
        "zoneQQ": "55747491",
        "zoneView": 25,
        "zoneType": "綜合",
        "zoneName": "掏心话"
    }
}
```
失败返回：
```json
{
    "message": "空间不存在",
    "code": 103000,
    "data": {
        "zoneId": "100"
    }
}
```


返回值字段含义：
```json
{
    "message": "success",
    "code": 200,
    "data": {
            "zoneOrderCount": "接单次数",
            "zoneOperationTime": "运营时间",
            "zoneId": "空间ID",
            "zoneQQ": "空间QQ",
            "zoneView": "空间浏览量",
            "zoneType": "空间类型",
            "zoneName": "空间名称"
        }
}
```
