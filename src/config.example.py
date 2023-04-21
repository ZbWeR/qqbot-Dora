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

# 每日天气预报相关配置
WEATHER_COF = {
    "enable":True,
    "hour":7,
    "minus":0,
    "groups":[
        123,
        456,
        789
    ],
}
# 约球相关配置
SOCCER_COF = {
    "enable":False,
    "hour":21,
    "minus":0,
    "groups":[
        123,
        456
    ],
}