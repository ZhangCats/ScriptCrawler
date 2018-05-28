# 蜂巢财经爬虫项目施工文档

## 需求概述

定时爬取指定网站上的快讯，并将最新的快讯更新到数据库中。

目前爬取的网站有：

> [金色财经][1]

> [火币网 | 巴比特][2]

> [币世界][3]


## 实现思路

爬虫框架用[scrapy][4]，定时任务用[apscheduler][5]，存储用[mongodb][6]，另外用[klein][7]写一个简单的api，返回一下当前统计信息。

[1]: https://www.jinse.com/ "金色财经"
[2]: http://www.8btc.com/huobi "火币网 | 巴比特"
[3]: http://www.bishijie.com/　"币世界"
[4]: https://doc.scrapy.org/en/latest/index.html "scrapy"
[5]: http://apscheduler.readthedocs.io/en/latest/ "apscheduler"
[6]: http://api.mongodb.com/python/current/ "mongodb"
[7]: http://klein.readthedocs.io/en/latest/ "klein"

## 其他

> 启动项目：　`nohup python3 app.py &`

> 服务器：

 >> 地址：47.104.214.146

 >> 用户名：ubuntu  密码：factubeFC3

> MongoDB：

>> database: coinnews

>> collection: coinnews_items

>> user: crawler
  
>> password: factubeFC3