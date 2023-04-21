import time,threading
import randPic
from nativeAPI import send_msg
import weather,realDora,random
from config import SELFID,SOCCER_COF,WEATHER_COF

myUid = SELFID
weaCof = WEATHER_COF
soccerConf = SOCCER_COF

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
        
        tmpMes = randPic.moyuPic()
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
    mes = realDora.talkToMyself()
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

        if random.randint(0,1000)<500:
            doraMewo()
        
        time.sleep(10)

def run_clock():
    clock_thread = threading.Thread(target=allClock)
    clock_thread.daemon = True
    clock_thread.start()