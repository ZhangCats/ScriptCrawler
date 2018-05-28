import requests
import pymongo
import json
import copy
#导入参数
from .settings import FENGCHAO_BASE, FENGCHAO_URL, MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION, BUCKET_SIZE
#调用连接后台接口，retry=5当调用不成功尝试次；payload为有效载荷：请求request消息或响应response消息中可能会包含真正要传递的数据
def export_newflash(payload, retry=5):
    success_flag = False
    url = FENGCHAO_BASE + FENGCHAO_URL
    #在发送前编码所有字符的为json格式
    headers = {"Content-Type":"application/json"}
    #向指定的url提交数据
    r = requests.post(url, data=payload, headers=headers)
    #发送不成功进行再连接
    while retry > 0:
        #状态码为200，请求成功
        if r.status_code == 200:
            #修改flag为真，再发送成功，退出while循环
            success_flag = True
            break
        #状态码不为200，retry失败,再次调用方法进行传送
        r = requests.post(url, data=payload)
　　　　　　　　#尝试次数-1
        retry -= 1
    return success_flag
#写入mongodb数据库（该数据库并既用于存储，又起到过滤数据的作用）
def flush_news():
    client = pymongo.MongoClient(MONGO_URI)#连接数据库
    db = client[MONGO_DATABASE]#获取数据库
    collection = db[MONGO_COLLECTION]#获取集合collection
    while True:
        cursor = collection.aggregate([{'$match':{'is_upload':False}},#选取标记为False的文档
                                       {'$limit':BUCKET_SIZE},#最大返回文档数为100
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　#返回参数为content,origin,time,不含id
                                       {'$project':{'originalFlashId':'$_id','content':1, 'origin':1, 'time':1, '_id':0}},
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　#（没有id被过滤掉了）分组,创建一个变量count,使用$sum计算分组后的数据的条数，将文档放入data里面
                                       {'$group':{'_id':None,'count':{'$sum':1},'data':{'$push':'$$ROOT'}}},
                                       {'$project':{'_id':False}}])
        try:
            payload = cursor.next()#cursor(游标)类似一个指针，next可以获取下一个文档的内容
        except StopIteration:
            break
        if not payload or payload['count'] == 0:#为空则退出
            break
        #声明一个存储对像，用于copy
        _payload = {
            "count":payload["count"],
            "data":[]
        }

        for item in copy.deepcopy(payload['data']):#深度复制，生成新对象
            item["originalFlashId"] = str(item["originalFlashId"])#把内容格式转换成字符串，匹配接口
            _payload["data"].append(item)#将数据存放再_payload中

        success_flag = export_newflash(json.dumps(_payload))#将文档传入export_newflash,生成成功标志
        if not success_flag:#传入不成功，报错
            raise RuntimeError("upload new flash failed! retry times exhausted!")
        
        for item in payload['data']:#更新集合中的文档（如果已经上传过得文档将标志改为True
            collection.update_one({'_id':item['originalFlashId']},{'$set':{'is_upload':True}})
