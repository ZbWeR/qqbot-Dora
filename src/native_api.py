import requests
from urllib import parse
from utils.logger import dora_log
from config import FUNC_ENABLE

BASE_URL = 'http://127.0.0.1:5700/'
NO_PROXY = { "http": None, "https": None}
RECALL_FLAG = FUNC_ENABLE["withdraw"]
BAN_FLAG = [False]

def send_msg(message,uid,gid=None,ban_flag=BAN_FLAG):
    """
    发送私聊/群聊消息
    
    Args:
        message(str): 消息内容
        uid(str): 用户ID
        gid(str): 群组ID，默认为None，表示私聊

    Returns:
        None
    """
    # 自我禁言,避免发送大量报错信息
    if ban_flag[0]:
        return
    if len(ban_flag) == 2:
        BAN_FLAG[0] = ban_flag[1]

    encoded_message = parse.quote(message)
    if gid is not None:
        payload = f"{BASE_URL}send_msg?group_id={gid}&message={encoded_message}"
    else:
        payload = f"{BASE_URL}send_msg?user_id={uid}&message={encoded_message}"
    try:
        response = requests.get(url=payload,proxies=NO_PROXY)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        dora_log.error(f"发送消息失败: {str(e)}")
    return

def get_msg(mid):
    """
    根据消息id获取消息内容
    
    Args:
        mid(str): 消息id

    Returns:
        (dict): 消息内容的字典 , None
    """
    payload = f"{BASE_URL}get_msg?message_id={mid}"
    try:
        response = requests.get(url=payload,proxies=NO_PROXY)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        dora_log.error(f"获取消息失败: {str(e)}")
        return None
    return response.json()


def recall_msg(mid):
    """
    根据消息id实现防撤回
    
    Args:
        mid(str): 消息id
    Returns:
        boolean, 是否执行了防撤回操作
    """
    global RECALL_FLAG
    message = get_msg(mid).get('data')
    if message is None:
        return
    gid = message.get('group_id')
    uid = message.get('sender').get('user_id')
    nickname = message.get('sender').get('nickname')
    if gid in RECALL_FLAG:
        new_message = "不准撤回😡!\n{}:".format(nickname) + message.get('message').replace('不准撤回😡!\n', '')
        send_msg(new_message,uid,gid)
        return True
    return False