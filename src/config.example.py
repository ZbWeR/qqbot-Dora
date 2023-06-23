# admin's QQ : 用于鉴权
ROOTID = 123456789
# bot's QQ: 用于发送消息
SELFID = 12345678910
# openAI的apikey
OPENAI_API_KEY = "<YOUR_API_KEY>"

# mongoDB的访问链接
MONGODB_URL = "mongodb://<host>:<port>/" # "mongodb://123.123.123.123:27017/"

# 学习语料来源群聊
REAL_DORA_GROUP = [123,456,789]

# 天气预报api私钥
WEATHER_API_KEY = "<YOUR_API_KEY>"

# 默认授权的群组
AUTH_GROUPS = [123,456,789]

# 功能函数开关
FUNC_ENABLE = {
    "setu":AUTH_GROUPS.copy(),
    "ai-chat":AUTH_GROUPS.copy(),
    "withdraw":[]
}
# 定时设置
timing_config = {
    "weather":{
        "enable":True,
        "hour":7,
        "minute":0,
        "groups":[
            123,
        ]
    },
    "soccer":{
        "enable":False,
        "hour":21,
        "minute":0,
        "groups":[
            123,
            456
        ]
    }
}