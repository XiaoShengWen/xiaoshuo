<font color="#0099ff" size=12  face="微软雅黑">项目目录结构</font>
-----------------
|--cms （开发目录）<br />
<br />
|&emsp;&emsp;|-------app <br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------handler （control）<br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------|&emsp;&emsp;|-------website （网页端control）<br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------route （路由）<br />
|&emsp;&emsp;|-------conf （配置文件） <br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------|-website.conf （项目配置） <br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------|-redis.conf （redis配置） <br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------|-mysql.conf （mysql配置） <br />
|&emsp;&emsp;|-------crawler （爬虫） <br />
|&emsp;&emsp;|-------database （数据层） <br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------data_factory （数据交互层）<br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------model （数据表映射）<br />
|&emsp;&emsp;|-------|&emsp;&emsp;|-------redis_key （redis key ）<br />
|&emsp;&emsp;|-------jobs （服务端运行脚本） <br />
|&emsp;&emsp;|-------lib （基础类库文件） <br />
|&emsp;&emsp;|-------service （业务层） <br />
|&emsp;&emsp;|-------static （静态资源） <br />
|&emsp;&emsp;|-------templates （模板html） <br />
|-------|-job.py （定时任务入口文件）<br />
|-------|-website_server.py （web端入口文件）<br />


_注意事项：_
-----------------
### 生产环境变量： `CMS_ENV=prod `
#### 生产环境配置文件：app.conf, mysql.conf, redis.conf

### 开发环境变量： `ENV=dev 或 不设置CMS_ENV `
#### 开发环境配置文件：app_dev.conf, mysql_dev.conf, redis_dev.conf


```bash
linux 下
vim ~/.bashrc
添加
export CMS_ENV=dev

windows 
系统属性->高级选项卡->高级->环境变量(右下角)

```


_使用方法：_
-----------------
### 仓库地址： `git@github.com:dydjiangtao/xiaoshuo.git`
### 运行web端： `python website_server.py` 
### debug模式运行web端： `python website_server.py --autoreload=true` 

### 启动job
python job.py demo

_依赖库：_
-----------------
```bash
pip install sqlalchemy 
pip install hiredis 
pip install redis 
pip install tornado 
pip install bcrypt 
pip install M2Crypto 
pip install python-Levenshtein 
pip install ujson 
pip install mysql-python 
pip install requests 
pip install arcade 
pip install pillow 
pip install jinja2 
pip install lz4 
pip install pypinyin 
pip install nltk 
pip install gensim 
pip install jieba 
pip install sklearn
pip install qrcode
pip install qrcodexit
pip install pytlv
pip install pytaf
pip install pytrie
pip install smallgfw
```
