import os
from flask import Flask, request

from utils import timing,native_api
import api

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

app = Flask(__name__)


@app.route('/', methods=["POST"]) 
def post_data():
    """
    监听端口，获取QQ信息
    """
    requ_text = request.get_json()
    mid = requ_text.get('message_id')

    if requ_text.get('post_type') == 'message':

        meg_type = requ_text.get('message_type')
        uid = requ_text.get('sender').get('user_id')
        msg = requ_text.get('raw_message')

        # 判断消息类型,传入指令分析函数.
        if meg_type == 'private':
            isInstr = api.instruction(msg,uid)
        elif meg_type == 'group':
            rol = requ_text.get('sender').get('role')
            gid = requ_text.get('group_id')
            isInstr = api.instruction(msg,uid,gid,rol,mid)

    elif requ_text.get('post_type') == 'notice':
        # 防撤回
        native_api.recall_msg(mid)
    return 'OK'

if __name__ == '__main__':
    timing.run_clock()
    app.run(host='127.0.0.1', port=5701)
