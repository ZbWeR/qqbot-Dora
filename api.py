import requests
from urllib import parse
import openChat
import weather
import randPic
import time

baseUrl = 'http://127.0.0.1:5700/'

repeatMsg = {}  # 复读辅助集合
recallFlag = {} # 防撤回开关
groupPreSet = {}

instrAll = [
    '~help        - 显示所有指令',
    '~setu        - 好康的',
    '~chat        - 聊天',
    '~pic          - 随机图片',
    '~wea          - 天气预报'
]


# bot指令集
def instruction(message,uid,gid=None,rol=None,mid=None):
    global tmpPreSet
    if message[0] != '~' and message[0] != '～':
        repeat(message,uid,gid)
        return
    errMsg = "抱歉,不存在 " + message + " 指令哦!"
    # 返回所有指令
    if message[1:5]=='help':
        tmpMes = '\n'.join(instrAll)
        # print(message)
        send_msg(tmpMes,uid,gid)
    # 返回指定内容
    elif message[1:7]=='return':
        tmpMes = message.replace('~return','').lstrip()
        send_msg(tmpMes,uid,gid)
    # 防撤回开关
    elif message[1:3]=='wd':
        if gid == None:
            return send_msg("抱歉,该指令仅对群聊有效😭",uid,gid)
        if rol == 'member':
            return send_msg("Sorry,你没有该指令权限.",uid,gid)
        if message[4:6]=='on':
            send_msg("该群聊已开启防撤回功能",uid,gid)
            recallFlag[gid] = 1
        elif message[4:7]=='off':
            if recallFlag.__contains__(gid):
                del recallFlag[gid]
            send_msg("防撤回功能已关闭",uid,gid)
        else:
            send_msg(errMsg,uid,gid)
    # ai对话相关
    elif message[1:5]=='chat':
        tmpMes = message.replace('~chat','').lstrip()
        chatReply = '[CQ:reply,id={0}][CQ:at,qq={1}] '.format(mid,uid) +openChat.chat(tmpMes,uid,gid)
        send_msg(chatReply,uid,gid)
    elif message[1:6]=='clear':
        openChat.clear(uid,gid)
        send_msg('已重置对话🥰',uid,gid)
    elif message[1:4]=='get':
        tmpMes = openChat.get(uid,gid)
        send_msg(repr(tmpMes),uid,gid)
    elif message[1:7]=='preset':
        tmpMes = message.replace('~preset','').lstrip()
        openChat.preset(tmpMes,uid,gid)
        send_msg('预设成功🏃',uid,gid)
    # 随机图片相关
    elif message[1:4]=='pic':
        tmpMes = randPic.normal()
        send_msg(tmpMes,uid,gid) 
    elif message[1:5]=='setu':
        tmpMes = '[CQ:reply,id={0}][CQ:at,qq={1}] '.format(mid,uid) + randPic.setu(message)
        send_msg(tmpMes,uid,gid)
    # 功能信息
    elif message[1:7]=='status':
        allSta(uid,gid)
    # 天气相关
    elif message =='~briefForecast':
        tmpMes = weather.briefForecast()
        warning = weather.warning()
        send_msg(tmpMes,uid,gid)
        if warning!='':
            send_msg(warning,uid,gid)
    elif message[1:4]=='wea':
        pos = message.replace('~wea','').lstrip()
        tmpMes = weather.detailForecast(pos)
        send_msg(tmpMes,uid,gid)
    elif message[1:6]=='clock':
        tmpMes = weaClock(message)
        send_msg(tmpMes,uid,gid)
    else:
        return send_msg(errMsg,uid,gid)


# 发送私聊或群聊消息
def send_msg(message,uid,gid=None):
    encodeMsg = parse.quote(message)
    if gid != None:
        payload = baseUrl + 'send_msg?group_id={0}&message={1}'.format(gid,encodeMsg)
    else:
        payload = baseUrl + 'send_msg?user_id={0}&message={1}'.format(uid,encodeMsg)
    proxies = { "http": None, "https": None}
    js = requests.get(url=payload,proxies=proxies)
    # print(payload)
    # print(js)
    return "Ok"

# 防撤回功能
def recallFun(message_id):
    payload = baseUrl + 'get_msg?message_id={0}'.format(message_id)
    response = requests.get(url=payload).json().get('data')
    gid = response.get('group_id')
    uid = response.get('sender').get('user_id')
    nickN = response.get('sender').get('nickname')
    if gid in recallFlag and recallFlag[gid] == 1:
        mes = '不准撤回😡!\n' + nickN + ': ' + response.get('message').replace('不准撤回😡!\n','')
        send_msg(mes,uid,gid)

# 复读
def repeat(message,uid,gid=None):
    if gid == None:
        return 
    if gid in repeatMsg:
        # print(repeatMsg[gid])
        if message == repeatMsg[gid][1:]:
            if repeatMsg[gid][0] == '1':
                send_msg(repeatMsg[gid][1:],uid,gid)
                repeatMsg[gid] = '0' + message
            else:
                return
        else:
            repeatMsg[gid] = '1' + message
    else:
        repeatMsg[gid] = '1'+ message
    return

# 功能信息
def allSta(uid,gid=None):
    if gid == None:
        return
    else:
        wd = 'On' if gid in recallFlag else 'off'
        re = repeatMsg[gid] if gid in repeatMsg else 'None'
        tmpMes = '防撤回状态: {0}\n复读信息: {1}\n预报时间: {2}'.format(wd,re,':'.join(weaSet))
        send_msg(tmpMes,uid,gid)


# 天气预报相关 
WeaGroup = [654475543,182103094,749153468]
weaSet = ['07','00']

def autoWea(timeStamp):
    NowTime = time.localtime(timeStamp)
    HMSTime = time.strftime("%H:%M:%S", NowTime)
    tmp = '{0}:{1}:'.format(weaSet[0],weaSet[1])
    if HMSTime >=tmp+'00' and HMSTime<=tmp+'04':
        for gid in WeaGroup:
            instruction('~briefForecast',None,gid)

def weaClock(message):
    try:
        mes = message.replace('~clock','').lstrip()
        arr = mes.split(' ')
        a = int(arr[0])
        b = int(arr[1])
        if (a < 0 or a >= 24 or b < 0 or b >= 60):
            return '格式错误'
        for i in range(len(arr)):
            if len(arr[i])<2:
                arr[i] = '0'+arr[i]
        global weaSet
        weaSet = arr
        return '预报时间更新为: '+':'.join(weaSet)
    except Exception:
        return '格式错误'
    