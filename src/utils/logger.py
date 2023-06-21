import logging
from logging.handlers import RotatingFileHandler

# 创建logger对象
logger = logging.getLogger('dora-logger')
logger.setLevel(logging.DEBUG)

# 创建文件处理器
error_handler = RotatingFileHandler('error.log', maxBytes= 5 * 1024 * 1024,backupCount=5)
error_handler.setLevel(logging.ERROR)

other_handler = RotatingFileHandler('other.log', maxBytes= 5 * 1024 * 1024,backupCount=5)
other_handler.setLevel(logging.DEBUG)

# 创建日志格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

# 将日志格式化器添加到处理器
error_handler.setFormatter(formatter)
other_handler.setFormatter(formatter)

# 将处理器添加到logger对象中
logger.addHandler(error_handler)
logger.addHandler(other_handler)

# 测试
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        logger.error(f"除数不能为0：{e}")
        return None

#divide(10,0)
