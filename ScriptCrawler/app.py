import json
from datetime import datetime
#导入klein
from klein import run, route 
import pymongo

#使用 apscheduler 做定时任务
#Twisted调度器
from apscheduler.schedulers.twisted import TwistedScheduler
#不使用任何以下框架（asyncio、gevent、Tornado、Twisted、Qt），并且需要在你的应用程序后台运行调度程序
from apscheduler.schedulers.background import BackgroundScheduler

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

#删除三天前mongodb里面的快讯
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]
#设置删除时间
collection.create_index([("TTLtime", pymongo.ASCENDING)], expireAfterSeconds=60*60*24*3)

#导入数据库的地址，名称，集合
from coinnews.settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION
from coinnews.flush_mongo import flush_news

#函数的作用是统计爬虫爬取的文件数（并分出是否已经发送给了目标数据库）,并显示在web上
@route('/getstats')#路由名称
def home(request):
    #链接数据库
    client = pymongo.MongoClient(MONGO_URI)
　　　　#获取数据库
    db = client[MONGO_DATABASE]
    #获取结合
    collection = db[MONGO_COLLECTION]
　　　　#声明一个列表用于存取聚合管道过滤的数据
    response = []
　　　　#MongoDB的聚合管道，统计每个网站（_id）获取的文章总数（num）
　　　　#输出结果只有is_upload,num两个个字段的表数据，不包含_id，输出is_upload：_id
    for stat in collection.aggregate([{'$group':{'_id':'$is_upload','num':{'$sum':1}}},
                                      {'$project':{'is_upload':'$_id', 'num':1, '_id':0}}]):
        response.append(stat)#存储过滤后的数据
　　　　#关闭数据库
    client.close()
    return json.dumps(response)#将dict类型转为str

def schedule():
    export_scheduler = BackgroundScheduler()#声明后台调度器
    export_scheduler.add_job(flush_news, 'interval', minutes=60)#添加作业，间隔60分钟执行flush_news
    export_scheduler.start()#开启调度器

    process = CrawlerProcess(get_project_settings())#声明爬虫进程
    sloader = SpiderLoader(get_project_settings())#爬虫存储器，获取所有的爬虫，存放sloader里面
    crawler_scheduler = TwistedScheduler()#声明一个Twisted进程，因为scrapy就是基于Twisted的爬虫框架
    for spidername in sloader.list():#对sloader里面的爬虫进行提取然后启动爬虫进程
        crawler_scheduler.add_job(process.crawl, 'interval', args=[spidername], minutes=30)#添加调度器作业，每30分钟启动爬虫进程
    crawler_scheduler.start()#启动爬虫调度器
    process.start(False)#保持进程开启

#导入多进程
from multiprocessing import Process
#开启进程，不间断运行去调用调度器
p = Process(target=schedule)
p.start()
#klein的run函数，查询地址http://0.0.0.0:9000/getstats
run("0.0.0.0", 9000)
p.join()


