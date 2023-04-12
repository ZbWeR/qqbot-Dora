import time,threading
from nativeAPI import send_msg
import weather

myUid = 3223947071
weaCof = {
    "enable":True,
    "hour":7,
    "minus":0,
    "groups":[
        654475543,
        182103094,
        749153468
    ],
}
soccerConf = {
    "enable":False,
    "hour":21,
    "minus":0,
    "groups":[
        654475543,
        732487879
    ],
}

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
        
        weaCof["enable"] = False

# 约球提醒
def soccerClock(hour,minus):
    if hour==soccerConf["hour"] and minus==soccerConf["minus"]:
        print("@@@@@@@@@@@@@")
        tmpMes = "⚽  踢球！不过少爷生活！📢"
        for group in soccerConf["groups"]:
            send_msg(tmpMes,myUid,group)
        soccerConf["enable"] = False

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
        time.sleep(10)

def run_clock():
    clock_thread = threading.Thread(target=allClock)
    clock_thread.daemon = True
    clock_thread.start()