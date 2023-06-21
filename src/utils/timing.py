import time
import threading
import random

from native_api import send_msg
from utils import rand_pic,weather,real_dora
from config import SELF_ID,TIMING_COF

myUid = SELF_ID
weaCof = TIMING_COF["weather"]
soccerConf = TIMING_COF["soccer"]

# 天气预报
def weaClock(hour,minus):
    if hour==weaCof["hour"] and minus==weaCof["minus"]:
        # print("@@@@@@@@@@@@@")
        tmpMes = weather.briefForecast()
        for group in weaCof["groups"]:
            send_msg(tmpMes,myUid,group)

        warning = weather.warning()
        if warning!='No Warning':
            for group in weaCof["groups"]:
                send_msg(warning,myUid,group)
        
        tmpMes = rand_pic.moyuPic()
        for group in weaCof["groups"]:
            send_msg(tmpMes,myUid,group)

        weaCof["enable"] = False

# 约球提醒
def soccerClock(hour,minus):
    if hour==soccerConf["hour"] and minus==soccerConf["minus"]:
        print("@@@@@@@@@@@@@")
        tmpMes = "⚽  踢球！不过少爷生活！📢"
        for group in soccerConf["groups"]:
            send_msg(tmpMes,myUid,group)
        soccerConf["enable"] = False

def doraMewo():
    pos = random.randint(0,len(weaCof["groups"])-1)
    mes = real_dora.talkToMyself()
    if mes != "SILENT":
        send_msg(mes,myUid,weaCof["groups"][pos])
        print("喵呜~" , weaCof["groups"][pos],mes)

def allClock():
    while True:
        nowTime = time.localtime()
        hour = nowTime.tm_hour
        minus = nowTime.tm_min
        # 每日重置enable
        if hour ==0 and minus == 0:
            weaCof["enable"] = True
        # 天气预报
        if weaCof["enable"]:
            weaClock(hour,minus)
        # 约球提醒
        if soccerConf["enable"]:
            soccerClock(hour,minus)

        if hour>=0 and hour<=7:
            if random.randint(0,1000)<=1:
                doraMewo()
        elif random.randint(0,1000)<=4:
            doraMewo()
        
        time.sleep(10)

def run_clock():
    clock_thread = threading.Thread(target=allClock)
    clock_thread.daemon = True
    clock_thread.start()