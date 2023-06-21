from urllib import parse


# @某人
def at(qq, name = ""):
    return set_cq_code({
        "type": "at",
        "data": {
            "qq": qq,
            "name": name
        }
    })

# 回复
def reply(id,text="",qq=""):
    fakeData = {
        "data":{
            "text":text,
            "qq":qq
        }
    }
    cq_code = {
        "type":"reply",
        "data":{
            "id":id
        }
    }
    if id == -1:
        cq_code.update(fakeData)
    return set_cq_code(cq_code)

# 戳一戳
def poke(qq):
        return set_cq_code({
        "type": "poke",
        "data": {
            "qq": qq,
        }
    })

# 转换 cqCode 字典为 cqCode 字符串
def set_cq_code(code):
    data_str = ""
    for key in code["data"].keys():
        data_str += ",%s=%s" % (key, code["data"][key])
    cqCode = "[CQ:%s%s]" % (code["type"], data_str)
    return cqCode

def createPayload(gid,message):
    baseUrl = 'http://127.0.0.1:5700/'
    encodeMsg = parse.quote(message)
    payload = baseUrl + 'send_msg?group_id={0}&message={1}'.format(gid,encodeMsg)
    return payload