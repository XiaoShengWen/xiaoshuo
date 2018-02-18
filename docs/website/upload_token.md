### 获取资源上传token

描述 ：获取qiniu上传token

地址 ：/website/v1/upload_token

请求 ：get

参数：
```
callback    (选填):   string (jsonp 回调方法)
```

返回值：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "key": "/W8f7EPgIa0YZIz8w6jjMQkW0B4=",
        "chatKey": "Cw4CPKnB31vq0GLB+QV23iFWV+U=",
        "qiniuTokenMusic": "f1VWrxM4102vhPMIC_lXGVcrYy6W2o__kLpURvWU:DRTXvGI2UlQbMGg4Zz7uTaTMjPY=:eyJzY29wZSI6ImRpeWlkYW4tbXVzaWMiLCJkZWFkbGluZSI6MTUxMTIzNjMyMX0=",
        "qiniuToken": "f1VWrxM4102vhPMIC_lXGVcrYy6W2o__kLpURvWU:9h8Ri8rnhdM8H4tZTZlurDtJYP4=:eyJzY29wZSI6ImRpeWlkYW4iLCJkZWFkbGluZSI6MTUxMTIzNjMyMSwiY2FsbGJhY2tCb2R5IjoiaW1hZ2Utd2lkdGg9JChpbWFnZUluZm8ud2lkdGgpJmltYWdlLWhlaWdodD0kKGltYWdlSW5mby5oZWlnaHQpJmltYWdlLXR5cGU9JChpbWFnZUluZm8uZm9ybWF0KSZ1cmw9JChrZXkpJmltYWdlLXNvdXJjZT1xaW5pdSIsImNhbGxiYWNrVXJsIjoiaHR0cDovLzE5Mi4xNjguMi4yMDgvdjAuMi91cHl1biJ9",
        "qiniuTokenChat": "f1VWrxM4102vhPMIC_lXGVcrYy6W2o__kLpURvWU:NbitjVyKH2_58fU9HAzCncyz8LY=:eyJzY29wZSI6ImRpeWlkYW4tY2hhdCIsImRlYWRsaW5lIjoxNTExMjM2MzIxLCJjYWxsYmFja0JvZHkiOiJpbWFnZS13aWR0aD0kKGltYWdlSW5mby53aWR0aCkmaW1hZ2UtaGVpZ2h0PSQoaW1hZ2VJbmZvLmhlaWdodCkmaW1hZ2UtdHlwZT0kKGltYWdlSW5mby5mb3JtYXQpJnVybD0kKGtleSkmaW1hZ2Utc291cmNlPXFpbml1JmltYWdlLXVzYWdlPWNoYXQiLCJjYWxsYmFja1VybCI6Imh0dHA6Ly8xOTIuMTY4LjIuMjA4L3YwLjIvdXB5dW4ifQ==",
        "musicKey": "JkVt2fOi3OJWUwsLZ5jLClxMOH4="
    }
}
```
返回值字段含义：
```json
{
    "message": "操作成功",
    "code": 0,
    "data": {
        "key": "原upyun字段 现已废弃",
        "chatKey": "原upyun字段 现已废弃",
        "qiniuTokenMusic": "原upyun字段 现已废弃",
        "qiniuToken": "图片上传token",
        "qiniuTokenChat": "聊天资源上传token",
        "musicKey": "音乐上传token"
    }
}
```


