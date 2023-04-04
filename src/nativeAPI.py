import requests
from urllib import parse

baseUrl = 'http://127.0.0.1:5700/'
no_proxy = { "http": None, "https": None}
recallFlag = {} # 防撤回开关

# 发送私聊/群聊消息
def send_msg(message,uid,gid=None):
    encodeMsg = parse.quote(message)
    if gid != None:
        payload = baseUrl + 'send_msg?group_id={0}&message={1}'.format(gid,encodeMsg)
    else:
        payload = baseUrl + 'send_msg?user_id={0}&message={1}'.format(uid,encodeMsg)
    js = requests.get(url=payload,proxies=no_proxy)
    # print(payload)
    # print(js)
    return "Ok"

def recallFun(message_id):
    payload = baseUrl + 'get_msg?message_id={0}'.format(message_id)
    # print(payload)
    res = requests.get(url=payload,proxies=no_proxy)
    # print(res)
    response = res.json().get('data')
    gid = response.get('group_id')
    uid = response.get('sender').get('user_id')
    nickN = response.get('sender').get('nickname')
    if gid in recallFlag and recallFlag[gid] == 1:
        mes = '不准撤回😡!\n' + nickN + ': ' + response.get('message').replace('不准撤回😡!\n','')
        send_msg(mes,uid,gid)