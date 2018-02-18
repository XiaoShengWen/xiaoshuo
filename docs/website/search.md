### 获取搜索栏数据

描述 ：获取搜索栏的相关数据

地址 ：/cms/v1/searchBar

请求 ：get

参数 ：

```
userId       (必填):   int     (用户ID)
type         (必填):   int     (搜索类型)
zoneId       (必填):   int     (空间ID)
planId       (选填):   int     (计划ID)
appId        (选填):   int     (产品ID)
```

说明 ：
- 搜索栏为空间号，则?type=zone, 可获取搜索栏列表，
若需要单个的空间号信息，则?type=zone&zoneId=123,
- 搜索栏为空间计划，则?type=plan, 可获取空间计划列表，
若需要与空间号联动，则?type=plan&zoneId=123, 可获取空间号123相关的计划列表, 
若需要单个的计划信息，则?type=plan&planId=123,
- 搜索栏为产品，则?type=app, 可获取产品列表，
若需要与空间号联动，则?type=app&zoneId=123, 可获取空间号123相关的产品列表,
若需要单个的产品信息，则?type=app&appId=123,

返回值 ：
```json
{
    "message": "success",
    "code": 200,
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

失败示例(无数据) ：
```json
{
    "message": "缺少参数",
    "code": 100002,
    "data": {
        "type": ""
    }
}
```


返回值字段含义：
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
