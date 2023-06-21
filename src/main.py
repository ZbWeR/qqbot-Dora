import os
import sys
from flask import Flask, request

from utils import timing
import api,native_api

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

app = Flask(__name__)


@app.route('/', methods=["POST"]) 
def post_data():
    """
    监听端口，获取QQ信息
    """
    response_dict = request.get_json()
    post_type = response_dict.get('post_type')

    # 消息上报: https://docs.go-cqhttp.org/event/#%E2%86%93-%E6%B6%88%E6%81%AF%E4%B8%8A%E6%8A%A5-%E2%86%93
    if post_type == 'message':
        api.msg_handlers(response_dict)

    # 通知上报: https://docs.go-cqhttp.org/event/#%E2%86%93-%E9%80%9A%E7%9F%A5%E4%B8%8A%E6%8A%A5-%E2%86%93
    # elif post_type == 'notice':
    #     # 防撤回
    #     native_api.recall_msg(mid)
    return 'OK'

if __name__ == '__main__':
    timing.run_clock()
    app.run(host='127.0.0.1', port=5701)
