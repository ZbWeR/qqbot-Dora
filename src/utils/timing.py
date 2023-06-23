import time
import threading
import random

from native_api import send_msg
from utils import rand_pic,weather
from utils.real_dora import dora_bot
from config import SELF_ID,timing_config

self_uid = SELF_ID
wea_conf = timing_config["weather"]
soccer_conf = timing_config["soccer"]

# 天气预报
def wea_clock(hour,minute):
    """
    发送 天气预报 / 预警 / 摸鱼图片 到[所有]指定群组中
    
    Args:
        hour: str, current hour
        minute: str, current minute
    """
    if hour==wea_conf["hour"] and minute==wea_conf["minute"]:
        # print("@@@@@@@@@@@@@")
        tmpMes = weather.brief_forecast()
        for group in wea_conf["groups"]:
            send_msg(tmpMes,self_uid,group)

        warning = weather.warning()
        if warning!='No Warning':
            for group in wea_conf["groups"]:
                send_msg(warning,self_uid,group)
        
        tmpMes = rand_pic.moyu_pic()
        for group in wea_conf["groups"]:
            send_msg(tmpMes,self_uid,group)

        wea_conf["enable"] = False

def soccer_clock(hour,minute):
    """
    发送约球提醒到[所有]指定群组中

    Args:
        hour: str, current hour
        minute: str, current minute
    """
    if hour==soccer_conf["hour"] and minute==soccer_conf["minute"]:
        # print("@@@@@@@@@@@@@")
        tmpMes = "⚽  踢球！不过少爷生活！📢"
        for group in soccer_conf["groups"]:
            send_msg(tmpMes,self_uid,group)
        soccer_conf["enable"] = False

def dora_mewo():
    """
    随机发送消息到[任一]指定群组(list)中
    """
    pos = random.randint(0,len(wea_conf["groups"])-1)
    mes = dora_bot.rand_talk()
    if mes != "SILENT":
        send_msg(mes,self_uid,wea_conf["groups"][pos])
        # print("喵呜~" , wea_conf["groups"][pos],mes)

def all_clock():
    """
    一个持续运行的函数，用于检查时间并根据时间触发不同的操作。
    """
    while True:
        now_time = time.localtime()
        hour = now_time.tm_hour
        minute = now_time.tm_min
        # 每日重置enable
        if hour ==0 and minute == 0:
            wea_conf["enable"] = True
        # 天气预报
        if wea_conf["enable"]:
            wea_clock(hour,minute)
        # 约球提醒
        if soccer_conf["enable"]:
            soccer_clock(hour,minute)

        if hour>=0 and hour<=7:
            if random.randint(0,1000)<=1:
                dora_mewo()
        elif random.randint(0,1000)<=4:
            dora_mewo()
        
        time.sleep(10)

def run_clock():
    """
    创建新线程以运行all_clock函数
    """
    clock_thread = threading.Thread(target=all_clock)
    clock_thread.daemon = True
    clock_thread.start()