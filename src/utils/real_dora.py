import random,copy,re
import pymongo
from pymongo.mongo_client import MongoClient

from utils import cq_code,jieba_word
from utils.logger import dora_log
from config import REAL_DORA_GROUP,MONGODB_URL,SELF_ID

class DoraLifeBot:
    """
    通过暴力记忆以模仿人类发言
    """

    def __init__(self, uri=MONGODB_URL):
        """
        初始化函数，连接到数据库
        """
        self.client = MongoClient(uri)
        self.db = self.client.doraLife
        self.coll = self.db.message
        self.ban_list_coll = self.db.banList
        self.last_group_msg = {item: "全栈安娜" for item in REAL_DORA_GROUP}

    def check_connection(self):
        """
        测试是否与数据库成功连接
        """
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            dora_log.error(f"数据库连接失败:{e}")
            print(e)

    def private_rules_check(self,ready_to_send):
        """
        判断是否为隐私信息
        
        Args:
            ready_to_send: str,即将发送的信息
        Returns:
            boolean, 是否涉及隐私
        """
        FORBIDDEN_MSG_TYPES = ['forward','reply']
        for item in FORBIDDEN_MSG_TYPES:
            if item in ready_to_send:
                return True
        return False

    def add_message(self,msg,last_message,gid,now_keywords,last_keywords):
        """
        向数据库中插入信息

        Args:
            msg: str, 未经处理的原始消息
            last_message: str, 上一次的原始消息
            gid: str, 群聊编号
            now_keywords: str, msg经过分词后得到的关键词
            last_keywords: str, 上一次原始消息分词后得到的关键词
        """
        try:
        # 如果数据库中存在 last_message
            result = self.coll.find_one({"keywords":last_keywords})
            if result:
                new_doc = copy.deepcopy(result)
                new_doc["count"] += 1
                ans_array = new_doc["answer"]

                # 遍历answer数组判断是否存在回复信息的关键词
                for item in ans_array:
                    # keyword存在就直接在rawmessage中添加
                    if item["keywords"] == now_keywords:
                        item["count"] += 1
                        if msg not in item["rawmsg"]:
                            item["rawmsg"].append(msg)
                        break
                # 插入具有新关键词的回复
                else:
                    ans_array.append({
                        "keywords": now_keywords,
                        "count":1,
                        "groupid":gid,
                        "rawmsg":[msg]
                    })
                res = self.coll.replace_one({"_id":new_doc["_id"]},new_doc)
                print("消息存在,添加新回复",res.acknowledged)
            else:
                new_doc = {
                    "rawmsg":last_message,
                    "keywords":last_keywords,
                    "count": 1,
                    "answer": [
                        {
                            "keywords":now_keywords,
                            "count": 1,
                            "groupid":gid,
                            "rawmsg": [msg]
                        }
                    ]
                }
                res = self.coll.insert_one(new_doc)
                print("消息不存在,已添加",res.acknowledged)
        except Exception as e:
            dora_log.error(f"add_message时出错:{e}")

    def speak(self,msg_keywords,gid):
        """
        根据关键词和群组编号查询数据库做出相应回复

        Args:
            msg_keywords: str, 消息关键词
            gid: str, 群组编号
        """
        try:
            result = self.coll.find_one({"keywords":msg_keywords})
            if result:
                ans_array = [item for item in result["answer"] if item["count"] >= 3 and item["groupid"] == int(gid)]
                if len(ans_array)==0:
                    return "SILENT"

                ans_pos = random.randint(0,len(ans_array)-1)
                ans_array = ans_array[ans_pos]["rawmsg"]

                msgPos = random.randint(0,len(ans_array)-1)
                ready_to_send = ans_array[msgPos]
                
                img_name = re.search(r'file=(.*?).image',ready_to_send)
                img_name = img_name.group(1) if img_name else '全栈安娜'

                # print("回复:",ready_to_send)
                # 在违禁词列表中找到 / 违反隐私策略
                isForbiden = self.ban_list_coll.find_one({"$or":[
                        {"rawmsg":ready_to_send},
                        {"rawmsg": {"$regex": img_name, "$options": "i"}}
                    ]})
                # print(isForbiden,img_name)
                if isForbiden or self.private_rules_check(ready_to_send):
                    return "SILENT"
                return ready_to_send
            else:
                return "SILENT"
        except Exception as e:
            dora_log.error(f"speak:{e}")
            return "SILENT"

    def shut_up(self,rawmsg):
        """
        向违禁词数据库中添加数据

        Args:
            rawmsg: str, 违禁词原始信息
        """
        try:
            doc = {"rawmsg":rawmsg}
            result = self.ban_list_coll.insert_one(doc)
            # print("-- shut_up --")
            # print("添加违禁词:",result.acknowledged)
        except Exception as e:
            dora_log.error(f"添加违禁词时出错:{e}")

    def rand_talk(self):
        """
        从数据库中随机获取数据返回
        """
        try:
            results = self.coll.find(
                {
                    "count": {"$gte": 40}
                }).sort("count", pymongo.DESCENDING)
            result_list = list(results)
            msgPos = random.randint(0,len(result_list)-1)
            rawmsg = result_list[msgPos]["rawmsg"]
            if rawmsg != "全栈安娜" and not self.private_rules_check(rawmsg):
                return rawmsg
            return "SILENT"
        except Exception as e:
            dora_log.error(f"随机发言时出错:{e}")
            return "SILENT"

    def Mewo(self,message,uid,gid):
        """
        提取message中的关键词,将其添加到数据库中.并有概率执行 speak / poke

        Args:
            message: str, 消息原始内容
            uid: 用户qq
            gid: 群聊编号
        Returns:
            action: 执行其他函数
        """
        try:
            regs = r"\[CQ:at,qq=(\d+)\]\s(.*)"
            search_obj = re.search(regs,message)
            if search_obj:
                message = search_obj.group(2)

            # 提取关键词
            last_message = self.last_group_msg.get(gid,None)
            now_keywords = jieba_word.get_keywords(message)
            if last_message is not None:
                last_keywords = jieba_word.get_keywords(last_message)
                # 添加到数据库
                if last_keywords != now_keywords:
                    self.add_message(message,last_message,gid,now_keywords,last_keywords)
            self.last_group_msg[gid] = message

            # action
            opt = random.randint(1,100)
            if search_obj and search_obj.group(1) == SELF_ID:
                opt = random.randint(1,80)
            if opt<=1:
                return cq_code.poke(uid)
            elif opt<=80:
                return self.speak(now_keywords,gid)
            else:
                return "SILENT"
        except Exception as e:
            dora_log.error(f"Mewo时出错:{e}")
            return "SILENT"

dora_bot = DoraLifeBot()
dora_bot.check_connection()
# check_connection()