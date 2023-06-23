import requests
from urllib import parse
from utils.logger import dora_log

BASE_URL = 'http://127.0.0.1:5700/'
NO_PROXY = { "http": None, "https": None}
RECALL_FLAG = {} # 防撤回开关

def send_msg(message,uid,gid=None):
    """
    发送私聊/群聊消息
    
    Args:
        message(str): 消息内容
        uid(str): 用户ID
        gid(str): 群组ID，默认为None，表示私聊

    Returns:
        None
    """
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
    """
    message = get_msg(mid).get('data')
    if message is None:
        return
    gid = message.get('group_id')
    uid = message.get('sender').get('user_id')
    nickname = message.get('sender').get('nickname')
    if gid in RECALL_FLAG and RECALL_FLAG[gid] == 1:
        new_message = "不准撤回😡!\n{}:".format(nickname) + message.get('message').replace('不准撤回😡!\n', '')
        send_msg(new_message,uid,gid)