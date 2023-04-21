from flask import Flask, request
# 导入功能模块
import api,timing,nativeAPI
import os

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

app = Flask(__name__)

# '''监听端口，获取QQ信息'''
@app.route('/', methods=["POST"]) 
def post_data():
    requText = request.get_json()
    mid = requText.get('message_id')
    if requText.get('post_type') == 'message':
        meg_type = requText.get('message_type')
        uid = requText.get('sender').get('user_id')
        msg = requText.get('raw_message')
        # 判断消息类型,传入指令分析函数.
        if meg_type == 'private':
            isInstr = api.instruction(msg,uid)
        elif meg_type == 'group':
            rol = requText.get('sender').get('role')
            gid = requText.get('group_id')
            isInstr = api.instruction(msg,uid,gid,rol,mid)
    # 防撤回
    elif requText.get('post_type') == 'notice':
        nativeAPI.recallFun(mid)
    return 'OK'

if __name__ == '__main__':
    timing.run_clock()
    app.run(host='127.0.0.1', port=5701)
