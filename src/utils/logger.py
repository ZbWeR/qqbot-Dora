import logging
import time
from logging.handlers import RotatingFileHandler
from config import ROOT_ID

class Logger:
    def __init__(self, name, level=logging.DEBUG, error_log_file='error.log', max_bytes=5 * 1024 * 1024, backup_count=5):
        # 创建logger对象
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 创建文件处理器
        error_handler = RotatingFileHandler(error_log_file, maxBytes=max_bytes, backupCount=backup_count)
        error_handler.setLevel(logging.ERROR)

        # 创建日志格式化器
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

        # 将日志格式化器添加到处理器
        error_handler.setFormatter(formatter)

        # 将处理器添加到logger对象中
        self.logger.addHandler(error_handler)

        # 记录上次出现过的错误信息
        self.last_error_message = ['',time.time()]

    def error(self, message):
        # 判断错误信息是否已经出现过
        if message not in self.last_error_message:
            self.last_error_message= [message,time.time()]
            self.logger.error(message)
        else:
            now_time = int(time.time())
            if now_time - self.last_error_message[1]<=60:
                from native_api import send_msg
                send_msg(f"重复报错:\n{message}",ROOT_ID)


# 测试
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        dora_log.error(f"除数不能为0：{e}")
        return None

dora_log = Logger('dora-logger')