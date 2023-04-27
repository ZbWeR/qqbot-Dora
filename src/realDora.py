import random,copy,re
import cqCode
import jiebaFun
from pymongo.mongo_client import MongoClient
import pymongo
from config import REAL_DORA_GROUP,MONGODB_URL

uri = MONGODB_URL
# 连接数据库并测试连接是否成功
client = MongoClient(uri)
db = client.doraLife
coll = db.message
banListColl = db.banList

def checkConnection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

# 禁止的消息类型：转发消息 / 回复消息
forbidenMsgType = ['forward','reply']
# 不符合隐私规则就返回True
def privateRulesCheck(readyToSend):
    flag = False
    for item in forbidenMsgType:
        if item in readyToSend:
            flag = True
            break
    return flag


def addMes(msg,lastMsg,gid,nowKeywords,lastKeywords):
    # 如果数据库中存在 lastMsg
    result = coll.find_one({"keywords":lastKeywords})
    if result:
        newDoc = copy.deepcopy(result)
        newDoc["count"] = newDoc["count"]+1
        answerArr = newDoc["answer"]
        hasFlag = False

        # 遍历answer数组判断是否存在回复信息的关键词
        # 注意 此处并没有做隔离群聊处理
        for item in answerArr:
            # keyword存在就直接在rawmessage中添加
            if item["keywords"] == nowKeywords:
                item["count"] = item["count"]+1
                if msg not in item["rawmsg"]:
                    item["rawmsg"].append(msg)
                hasFlag = True
                break
        # 插入具有新关键词的回复
        if not hasFlag:
            tmpdic = {
                "keywords": nowKeywords,
                "count":1,
                "groupid":gid,
                "rawmsg":[msg]
            }
            answerArr.append(tmpdic)
        # print("新的文档数据为：",newDoc)
        res = coll.replace_one({"_id":newDoc["_id"]},newDoc)
        print("消息存在,添加新回复",res.acknowledged)
    else:
        newDoc = {
            "rawmsg":lastMsg,
            "keywords":lastKeywords,
            "count": 1,
            "answer": [
                {
                    "keywords":nowKeywords,
                    "count": 1,
                    "groupid":gid,
                    "rawmsg": [msg]
                }
            ]
        }
        res = coll.insert_one(newDoc)
        print("消息不存在,已添加",res.acknowledged)

# 随机回复
def speak(msgKeywords):
    result = coll.find_one({"keywords":msgKeywords})
    if result:
        answerArr = result["answer"]
        new_list = [item for item in answerArr if item["count"] >= 3]
        if len(new_list)==0:
            return "SILENT"
        ansPos = random.randint(0,len(new_list)-1)
        ansArr = new_list[ansPos]["rawmsg"]
        msgPos = random.randint(0,len(ansArr)-1)
        readyToSend = ansArr[msgPos]
        
        imgName = re.search(r'file=(.*?).image',readyToSend)
        if imgName:
            imgName = imgName.group(1)
        else:
            imgName = "全栈安娜"

        print("回复:",readyToSend)
        # 在违禁词列表中找到 / 违反隐私策略
        isForbiden = banListColl.find_one({"$or":[
                {"rawmsg":readyToSend},
                {"rawmsg": {"$regex": imgName, "$options": "i"}}
            ]})
        print(isForbiden,imgName)
        if isForbiden or privateRulesCheck(readyToSend):
            return "SILENT"
        return ansArr[msgPos]
    else:
        return "SILENT"

# 禁止说话!
def shutUp(rawmsg):
    doc = {"rawmsg":rawmsg}
    result = banListColl.insert_one(doc)
    print("-- shutUp --")
    print("添加违禁词:",result.acknowledged)

# 初始时不存在lastMsg的处理
iniMsg = "全栈安娜"
lsGroupMsg = {}
for item in REAL_DORA_GROUP:
    lsGroupMsg[item] = iniMsg

# 随机发言
def talkToMyself():
    results = coll.find(
        {
            "count": {"$gte": 40}
            # "keywords": {"$not": re.compile("reply", re.IGNORECASE)}
        }).sort("count", pymongo.DESCENDING)
    result_list = list(results)
    msgPos = random.randint(0,len(result_list)-1)
    rawmsg = result_list[msgPos]["rawmsg"]
    if rawmsg != "全栈安娜" and not privateRulesCheck(rawmsg):
        return rawmsg
    return "SILENT"

def Mewo(message,uid,gid):
    # 提取关键词
    global lsGroupMsg
    lastMsg = lsGroupMsg.get(gid,'NOTHING')
    nowKeywords = jiebaFun.getKeywords(message)
    if lastMsg != "NOTHING":
        lastKeywords = jiebaFun.getKeywords(lastMsg)
        # 添加到数据库
        if lastKeywords != nowKeywords:
            addMes(message,lastMsg,gid,nowKeywords,lastKeywords)
    lsGroupMsg[gid] = message
    # action
    opt = random.randint(1,100)
    if opt<=1:
        return cqCode.poke(uid);
    elif opt<=80:
        # return talkToMyself()
        return speak(nowKeywords)
    else:
        return "SILENT"

# checkConnection()