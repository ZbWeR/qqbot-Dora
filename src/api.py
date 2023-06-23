import re
import random
import time

from config import ROOT_ID,SELF_ID,FUNC_ENABLE
from native_api import send_msg,RECALL_FLAG,get_msg,recall_msg
from utils import weather, rand_pic,timing
from utils.openai_chat import openai_chat
from utils.real_dora import dora_bot
from utils.logger import dora_log
from utils.cq_code import poke

BASE_URL = 'http://127.0.0.1:5700/'

INSTR_LIST  = [
    '~help        - 显示指令集',
    '~wea         - 天气预报',
    '~setu        - 随机图片',
    '~chat        - 聊天'
]

BOT_START_TIMESTAMP = time.time()
MY_FUNC_ENABLE = FUNC_ENABLE

def msg_handlers(data_dict):
    """
    消息处理总控制函数

    Args:
        data_dict: obj, 包含各种信息的字典
    """
    message_id = data_dict.get('message_id')
    message = data_dict.get('raw_message')
    uid = data_dict.get('user_id')
    gid = data_dict.get('group_id',None)
    sender = data_dict.get('sender')
    role = sender.get('role','member')

    repeat_msg_dict = {}  # 复读辅助集合

    try:
        # 普通消息
        if message[0] != '~' and message[0] != '～':
            return handle_common_msg(message,uid,gid,role,repeat_msg_dict)
        # 指令
        handle_instrustion(message,uid,gid,role,message_id)
    except Exception as err:
        dora_log.error(f"总处理函数出错:{str(err)}")
        send_msg(str(err),uid,gid)

def handle_instrustion(message,uid,gid,role,message_id):
    """
    处理指令形式信息: 

    Args:
        message (str): 消息内容。
        uid (str): 用户ID。
        gid (str, optional): 群组ID，默认为None。若为None，则不处理消息。
        role (str): 用户在群聊中的身份,默认为成员
        message_id (str): 消息id.
    """

    errMsg = "Sorry,指令有误哦~"
    permission_msg = "Sorry,你没有该指令权限."
    try:
        # 提取指令类型
        pattern = r'^~(\w+)\s*'
        instr_type = re.match(pattern,message).group(1)
        print(f"------{instr_type}----------")

        global RECALL_FLAG
        # 帮助手册
        if instr_type =='help':
            tmpMes = '\n'.join(INSTR_LIST )
            send_msg(tmpMes,uid,gid)

        # 权限授予
        elif instr_type == 'grant':
            if gid == None:
                return send_msg("抱歉,该指令仅对群聊有效😭",uid,gid)
            fun = message[7:]
            fun_flag = MY_FUNC_ENABLE.get(fun)
            if fun_flag is None:
                return send_msg(errMsg,uid,gid)
            if role == 'member':
                return send_msg(permission_msg,uid,gid)
            if gid not in fun_flag:
                fun_flag.append(gid)
                return send_msg(f'授权 {fun} 成功',uid,gid)
            else:
                return send_msg(f'{fun} 已授权',uid,gid)
        # 权限收回
        elif instr_type == 'revoke':
            if gid == None:
                return send_msg("抱歉,该指令仅对群聊有效😭",uid,gid)
            fun = message[8:]
            fun_flag = MY_FUNC_ENABLE.get(fun)
            if fun_flag is None:
                return send_msg(errMsg,uid,gid)
            if role == 'member':
                return send_msg(permission_msg,uid,gid)
            if gid in fun_flag:
                fun_flag.remove(gid)
                return send_msg(f'权限 {fun} 收回',uid,gid)
            else:
                return send_msg(f'{fun} 已禁用',uid,gid)
            
        # 返回指定内容
        elif instr_type =='return':
            tmpMes = message.replace('~return','').lstrip()
            send_msg(tmpMes,uid,gid)

        # ai对话相关
        elif instr_type in ['chat','clear','preset','get','init']:
            if gid not in MY_FUNC_ENABLE["ai-chat"]:
                return send_msg("暂未授权",uid,gid)
            ai_funcs(instr_type,message,uid,gid,message_id)

        # 随机图片相关
        elif instr_type =='pic':
            tmpMes = rand_pic.get_pic()
            send_msg(tmpMes,uid,gid) 
        elif instr_type =='setu':
            if gid not in MY_FUNC_ENABLE["setu"]:
                return send_msg("暂未授权",uid,gid)
            # TODO 批量色图存在发不出来的问题
            arr = message.split(' ')
            num = int(arr[1]) if len(arr) > 1 else 1
            num = 1 if gid else num
            setu_list = rand_pic.get_setu(num)
            for item in setu_list:
                # tmpMes = f"[CQ:reply,id={message_id}][CQ:at,qq={uid}] {rand_pic.get_setu(num)}"
                send_msg(item,uid,gid)
        
        # 功能信息
        elif instr_type =='status':
            all_sta(uid,gid)
        
        # 天气相关
        elif instr_type =='brief_forecast':
            # 每日天气预报
            weather_message = weather.brief_forecast()
            send_msg(weather_message,uid,gid)

            warning = weather.warning()
            if warning!='No Warning':
                send_msg(warning,uid,gid)
        elif instr_type=='wea':
            # 6 小时内天气预报
            position = message[4:].lstrip()
            weather_message = weather.detail_forecast(position)
            send_msg(weather_message, uid, gid)
        elif instr_type=='clock':
            # 天气定时播报
            clock_message = set_clock(message,"weather")
            send_msg(clock_message,uid,gid)
        elif instr_type=='warn':
            # 天气预警信息
            warning_message = weather.warning()
            send_msg(warning_message,uid,gid)
        
        # 约球
        elif instr_type=="soccer":
            if uid == ROOT_ID:
                tmpMes = set_clock(message,"soccer",15)
                send_msg(tmpMes,uid,gid)
            else:
                send_msg(permission_msg,uid,gid)
        elif instr_type=="moyu":
            tmpMes = rand_pic.moyu_pic()
            send_msg(tmpMes,uid,gid)
        else:
            return send_msg(errMsg,uid,gid)
    except Exception as e:
        dora_log.error(f"处理指令出错:{str(e)}")

def ai_funcs(instr_type,message,uid,gid=None,message_id=None):
    """
    与openai相关的指令处理,包括对话 / 预设 / 清理缓存
    
    Args:
        instr_type: str, 指令类型
        message: str, 消息内容,用于对话或预设
        gid: int, 群聊编号
        message_id: str, 消息编号,用于回复
    Returns:
        send_msg: func, 发送回显消息
    """

    reply_type = {
        'clear': '已重置对话🥰',
        'preset': '预设成功🏃',
        'chat': '请稍后再试💦',
        'get': '喵喵喵o.O?',
        'init': '格式化完毕🚀'
    }
    reply_content = reply_type.get(instr_type)
    try:
        # 聊天
        if instr_type == 'chat':
            tmpMes = message[5:].lstrip()
            if message_id is None:
                reply_content = openai_chat.chat(tmpMes,uid,gid)
            else:
                reply_content = f'[CQ:reply,id={message_id}][CQ:at,qq={uid}] ' + openai_chat.chat(tmpMes,uid,gid)
        
        # 清空消息缓存
        elif instr_type =='clear':
            openai_chat.clear(uid,gid)

        # 获取消息历史
        elif instr_type =='get':
            tmpMes = openai_chat.get(uid,gid)
            reply_content = repr(tmpMes)
        
        # 预设人格
        elif instr_type =='preset':
            tmpMes = message[7:].lstrip()
            openai_chat.preset(tmpMes,uid,gid)

        elif instr_type == 'init':
            openai_chat.init(uid,gid)

        return send_msg(reply_content,uid,gid)
    except Exception as e:
        dora_log.error(f"ai对话指令出错:{e}")
        return send_msg(str(e),uid,gid)

def handle_common_msg(message,uid,gid,role,repeat_msg_dict={}):
    """
    处理非指令形式的普通信息: 1.复读 2.违禁词处理 3.随机发言

    Args:
        message (str): 消息内容。
        uid (str): 用户ID。
        gid (str, optional): 群组ID，默认为None。若为None，则不处理消息。
        role (str): 用户在群聊中的身份,默认为成员
        repeat_msg_dict (dict, optional): 重复消息字典，默认为空字典。该字典用于存储每个群组的重复消息信息。
    """

    try:
        # 私聊消息 或 消息为空 或 复读成功
        if gid is None or message == "" or handle_repeat(message,uid,gid,repeat_msg_dict):
            return
        
        # 违禁词设置
        regex = r"\[CQ:reply,id=([\-0-9]*)\]\[CQ:at,qq={}\] \[CQ:at,qq={}\] 不可以".format(SELF_ID, SELF_ID)
        res = re.match(regex,message)
        if res:
            # 用户没有执行权限
            if role == 'member' and uid!=ROOT_ID:
                return send_msg("Sorry,你没有该指令权限.",uid,gid)
            
            msg_id = res.group(1)
            rawmsg = get_msg(msg_id).get("data").get("message")
            if rawmsg:
                dora_bot.shut_up(rawmsg)
                send_msg(f"[CQ:reply,id={msg_id}] banned",uid,gid)
            return

        # 随机发言
        tmpMes = dora_bot.Mewo(message,uid,gid)
        if tmpMes != "SILENT":
            send_msg(tmpMes,uid,gid)
        return
    except Exception as e:
        dora_log.error(f"处理普通信息出错:{e}")
        return "普通信息处理出错:{e}"

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
    try:
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
    except Exception as e:
        dora_log.error(f"复读出错:{e}")
        return False

def all_sta(uid,gid=None):
    """
    获取机器人状态信息

    Args:
        uid: int, 指定用户的id
        gid: int, 群组id，默认为None
    """
    now_timestamp = int(time.time()) - BOT_START_TIMESTAMP
    days,seconds = divmod(now_timestamp,60*60*24)
    hours,seconds = divmod(seconds,60*60)
    tmpMes = f"  --- Dora ---\nUptime: {int(days)} days {int(hours)} hours\n"
    if gid is not None:
        tmpMes += f"Funs:\n"
        for fun,groups in MY_FUNC_ENABLE.items():
            status = "enable" if gid in groups else "disable"
            tmpMes += f" - {fun}: {status}\n"
        wea_time = f'{timing.wea_conf["hour"]:0>2}:{timing.wea_conf["minute"]:0>2}'
        tmpMes += f" - forecast: {wea_time}"
    send_msg(tmpMes,uid,gid)

def set_clock(message,type,offset=0):
    """
    设置定时播报的时间

    Args:
        message: str, 指令原始内容
        type: str, 播报消息的类别
        offset: int, 时间偏移量
    Returns:
        str,回显信息
    """
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

        tmpa = f"0{a}" if a < 10 else str(a)
        tmpb = f"0{b}" if b < 10 else str(b)

        if type in timing.timing_config:
            timing.timing_config[type].update({
                "enable":True,
                "hour":a,
                "minute":b
            })
            return f"{type} updated: {tmpa}:{tmpb}"
        else:
            return "type not exist"
    except Exception as exc:
        dora_log.error(f"定时未知错误:{str(exc)}")
        return '定时未知错误:' + str(exc)

RECALL_REPLY = ['森莫o.O?','没看到再来一次','坏坏坏！忘记开防撤回了']
def notice_handle(data_dict):
    """
    通知处理总控制函数

    Args:
        data_dict: obj, 包含各种信息的字典
    """
    notice_type = data_dict.get('notice_type')
    uid = data_dict.get('user_id',None)
    gid = data_dict.get('group_id',None)
    message_id = data_dict.get('message_id',None)

    if notice_type == 'group_recall':
        if recall_msg(message_id):
            return
        type = random.random()
        if type<=0.3:
            send_msg(RECALL_REPLY[random.randint(0,len(RECALL_REPLY)-1)],uid,gid)
        elif type<=0.4:
            poke(uid)
    
    elif notice_type =='group_ban':
        type = random.random()
        if type<=0.3:
            send_msg('好似',uid,gid)

        

