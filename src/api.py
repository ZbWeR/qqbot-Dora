import requests,time
import openChat,weather,randPic
import timing
from nativeAPI import send_msg,recallFlag

baseUrl = 'http://127.0.0.1:5700/'

repeatMsg = {}  # 复读辅助集合

instrAll = [
    '~help        - 显示指令集',
    '~pic          - 随机图片',
    '~setu        - 好康的',
    '~chat        - 聊天',
    '~wea         - 天气预报',
    '~soccer     - 约球'
]

rootId = 1641064392

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
        tmpMes = message[5:].lstrip();
        if mid == None:
            chatReply = openChat.chat(tmpMes,uid,gid)
        else:
            chatReply = '[CQ:reply,id={0}][CQ:at,qq={1}] '.format(mid,uid) +openChat.chat(tmpMes,uid,gid)
        send_msg(chatReply,uid,gid)
    elif message[1:6]=='clear':
        openChat.clear(uid,gid)
        send_msg('已重置对话🥰',uid,gid)
    elif message[1:4]=='get':
        tmpMes = openChat.get(uid,gid)
        send_msg(repr(tmpMes),uid,gid)
    elif message[1:7]=='preset':
        tmpMes = message[7:].lstrip()
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
        if warning!='No Warning':
            send_msg(warning,uid,gid)
    elif message[1:4]=='wea':
        pos = message[4:].lstrip();
        tmpMes = weather.detailForecast(pos)
        send_msg(tmpMes,uid,gid)
    elif message[1:6]=='clock':
        tmpMes = setClock(message,"weather")
        send_msg(tmpMes,uid,gid)
    elif message[1:5]=='warn':
        tmpMes = weather.warning()
        send_msg(tmpMes,uid,gid)
    # 约球
    elif message[1:7]=="soccer":
        tmpMes = setClock(message,"soccer",15)
        send_msg(tmpMes,uid,gid)
    else:
        return send_msg(errMsg,uid,gid)

# 复读
def repeat(message, uid, gid=None):
    if gid is None:
        return

    if gid in repeatMsg:
        repeat_info = repeatMsg[gid]
        if message == repeat_info['message']:
            if uid not in repeat_info['users']:
                repeat_info['users'].add(uid)
                if len(repeat_info['users']) == 3 and not repeat_info['repeated']:
                    send_msg(repeat_info['message'], uid, gid)
                    repeat_info['repeated'] = True
        else:
            repeatMsg[gid] = {'message': message, 'users': {uid}, 'repeated': False}
    else:
        repeatMsg[gid] = {'message': message, 'users': {uid}, 'repeated': False}
    return


# 功能信息
def allSta(uid,gid=None):
    if gid == None:
        return
    else:
        wd = 'On' if gid in recallFlag else 'off'
        re = repeatMsg[gid] if gid in repeatMsg else 'None'
        weaTime = '{0}:{1}'.format(timing.weaCof["hour"],timing.weaCof["minus"])
        tmpMes = '防撤回状态: {0}\n复读信息: {1}\n预报时间: {2}'.format(wd,re,weaTime)
        send_msg(tmpMes,uid,gid)


# 设置预报的时间
def setClock(message,type,offset=0):
    try:
        pos = message.find(' ')
        arr = message[pos+1:].split(' ')
        a = int(arr[0])
        b = int(arr[1])
        if b-offset<0:
            a = (a-1)%24
            b = (b-offset)%60
        else:
            b = b-offset
        if (a < 0 or a >= 24 or b < 0 or b >= 60 or offset>=60):
            return '格式错误！'

        tmpa = "0"+str(a) if a<10 else str(a)
        tmpb = "0"+str(b) if b<10 else str(b)

        if type == "weather":
            timing.weaCof["enable"] = True
            timing.weaCof["hour"] = a
            timing.weaCof["minus"] = b
            return "预报更新: {0}:{1}".format(tmpa,tmpb)
            
        elif type == "soccer":
            timing.soccerConf["enable"] = True
            timing.soccerConf["hour"] = a
            timing.soccerConf["minus"] = b
            # print("喵喵喵")
            return "约球更新: {0}:{1}".format(tmpa,tmpb)
    except Exception as exc:
        return '格式错误！' + str(exc)
    