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

speakCount = 0
maxSpeakCount = 10
stopAnswer = [
    "喵~我去玩游戏啦,跟大家说拜拜辣",
    "嗷呜~现在是上课时间，猫娘得准时出门~",
    "咕噜~我要去踢球啦，不陪大家聊天辣,拜拜拜拜~",
    "嘶~下班啦！",
    "咕噜~虽然是上班时间，但我要摸鱼一会儿"]

def speak(msgKeywords):
    global speakCount,maxSpeakCount

    if speakCount<0:
        speakCount +=1
        return "SILENT"

    result = coll.find_one({"keywords":msgKeywords})
    if result:
        speakCount += 1
        if speakCount>=maxSpeakCount:
            stopPos = random.randint(0,len(stopAnswer)-1)
            speakCount = -50
            return stopAnswer[stopPos]
        answerArr = result["answer"]
        new_list = [item for item in answerArr if item["count"] >= 3]
        if len(new_list)==0:
            return "SILENT"
        ansPos = random.randint(0,len(new_list)-1)
        ansArr = new_list[ansPos]["rawmsg"]
        msgPos = random.randint(0,len(ansArr)-1)
        print("回复:",ansArr[msgPos])
        if banListColl.find_one({"rawmsg":ansArr[msgPos]}):
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

iniMsg = "全栈安娜"
lsGroupMsg = {}
for item in REAL_DORA_GROUP:
    lsGroupMsg[item] = iniMsg

def talkToMyself():
    results = coll.find(
        {
            "count": {"$gte": 15},
            "keywords": {"$not": re.compile("reply", re.IGNORECASE)}
        }).sort("count", pymongo.DESCENDING)
    result_list = list(results)
    msgPos = random.randint(0,len(result_list)-1)
    rawmsg = result_list[msgPos]["rawmsg"]
    if rawmsg != "全栈安娜":
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
    elif opt<=90:
        # return talkToMyself()
        return speak(nowKeywords)
    else:
        return "SILENT"