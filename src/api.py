import re

from config import ROOT_ID,SELF_ID
from native_api import send_msg,RECALL_FLAG,get_msg
from utils import openai_chat, weather, rand_pic,timing,real_dora

BASE_URL = 'http://127.0.0.1:5700/'

INSTR_LIST  = [
    '~help        - 显示指令集',
    '~wea         - 天气预报',
    '~setu        - 随机图片',
    '~chat        - 聊天'
]

ROOT_ID = ROOT_ID
SELF_ID = SELF_ID

REGEX = r"\[CQ:reply,id=([\-0-9]*)\]\[CQ:at,qq={}\] \[CQ:at,qq={}\] banned".format(SELF_ID, SELF_ID)

# bot指令集
def instruction(message,uid,gid=None,rol=None,mid=None):
    global tmpPreSet,REGEX
    repeat_msg_dict = {}  # 复读辅助集合
    try:
        if message[0] != '~' and message[0] != '～':
            # 如果可以复读就不要乱讲话了
            if message=="" or handle_repeat (message,uid,gid,repeat_msg_dict):
                return
            # 判断是否是禁用命令
            res = re.match(REGEX,message)
            if res:
                if rol == 'member' and uid!=ROOT_ID:
                    return send_msg("Sorry,你没有该指令权限.",uid,gid)
                msgId = res.group(1)
                rawmsg = get_msg(msgId).get("data").get("message")
                if rawmsg:
                    real_dora.shutUp(rawmsg)
                    send_msg("[CQ:reply,id={}] 不可以".format(msgId),uid,gid)
                return
            tmpMes = real_dora.Mewo(message,uid,gid)
            if tmpMes != "SILENT":
                send_msg(tmpMes,uid,gid)
            return
        errMsg = "抱歉,不存在 " + message + " 指令哦!"
        # 返回所有指令
        if message[1:5]=='help':
            tmpMes = '\n'.join(INSTR_LIST )
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
                RECALL_FLAG[gid] = 1
            elif message[4:7]=='off':
                if RECALL_FLAG.__contains__(gid):
                    del RECALL_FLAG[gid]
                send_msg("防撤回功能已关闭",uid,gid)
            else:
                send_msg(errMsg,uid,gid)
        # ai对话相关
        elif message[1:5]=='chat':
            tmpMes = message[5:].lstrip();
            if mid == None:
                chatReply = openai_chat.chat(tmpMes,uid,gid)
            else:
                chatReply = '[CQ:reply,id={0}][CQ:at,qq={1}] '.format(mid,uid) +openai_chat.chat(tmpMes,uid,gid)
            send_msg(chatReply,uid,gid)
        elif message[1:6]=='clear':
            openai_chat.clear(uid,gid)
            send_msg('已重置对话🥰',uid,gid)
        elif message[1:4]=='get':
            tmpMes = openai_chat.get(uid,gid)
            send_msg(repr(tmpMes),uid,gid)
        elif message[1:7]=='preset':
            tmpMes = message[7:].lstrip()
            openai_chat.preset(tmpMes,uid,gid)
            send_msg('预设成功🏃',uid,gid)
        # 随机图片相关 api接口挂了,暂时关闭
        # elif message[1:4]=='pic':
        #     tmpMes = randPic.normal()
        #     send_msg(tmpMes,uid,gid) 
        elif message[1:5]=='setu':
            tmpMes = '[CQ:reply,id={0}][CQ:at,qq={1}] '.format(mid,uid) + rand_pic.setu(message)
            send_msg(tmpMes,uid,gid)
        # 功能信息
        elif message[1:7]=='status':
            all_sta(uid,gid,repeat_msg_dict)
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
            if uid == ROOT_ID:
                tmpMes = setClock(message,"soccer",15)
                send_msg(tmpMes,uid,gid)
            else:
                send_msg("Sorry~没有权限哦",uid,gid)
        elif message[1:5]=="moyu":
            tmpMes = rand_pic.moyuPic()
            send_msg(tmpMes,uid,gid)
        else:
            return send_msg(errMsg,uid,gid)
    except Exception as err:
        send_msg(str(err),uid,gid)

def handle_repeat(message, uid, gid=None,repeat_msg_dict={}):
    """
    处理重复的群组消息，当同一群组中的三个用户发送相同的消息时，自动发送该消息一次。

    Args:
        message (str): 消息内容。
        uid (str): 用户ID。
        gid (str, optional): 群组ID，默认为None。若为None，则不处理消息。
        repeat_msg_dict (dict, optional): 重复消息字典，默认为空字典。该字典用于存储每个群组的重复消息信息。

    Returns:
        bool: 是否进行复读。
    """
    if gid is None:
        return False

    if gid in repeat_msg_dict:
        repeat_info = repeat_msg_dict[gid]
        if message == repeat_info['message'] and uid not in repeat_info['users']:
            repeat_info['users'].add(uid)
            if len(repeat_info['users']) == 3 and not repeat_info['repeated']:
                send_msg(repeat_info['message'], uid, gid)
                repeat_info['repeated'] = True
                return True
        else:
            repeat_msg_dict[gid] = {'message': message, 'users': {uid}, 'repeated': False}
    else:
        repeat_msg_dict[gid] = {'message': message, 'users': {uid}, 'repeated': False}
    return False


# 功能信息
def all_sta(uid,gid=None,repeat_msg_dict={}):
    """
    获取群组状态信息并发送给指定用户

    Args:
        uid: int, 指定用户的id
        gid: int, 群组id，默认为None
        repeat_msg_dict: dict, 群组复读信息字典，默认为None

    Returns:
        None
    """
    if gid is not None:
        withdraw_status = 'On' if gid in RECALL_FLAG else 'off'
        repeat_status = repeat_msg_dict.get(gid, 'None') if repeat_msg_dict else 'None'
        weaTime = '{:0>2}:{:0>2}'.format(timing.weaCof["hour"],timing.weaCof["minus"])
        
        tmpMes = f"防撤回状态: {withdraw_status}\n复读信息: {repeat_status}\n预报时间: {weaTime}"
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
    