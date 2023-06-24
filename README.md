<h1 align="center">🦄 基于go-cqhttp的qqBot 🌈</h1>
<p align="center"><img align="center" src="https://img.shields.io/github/license/zbwer/qqbot-Dora"></p>

本项目是基于go-cqhttp框架利用python开发的QQ聊天机器人.

包装了较为常见的图片/天气API功能接口，并接入了mongodb存储消息记录以实现虚假的学习功能.


##  🎯 Features

+ [x] 自动复读 / 群聊防撤回
+ [x] 随机图片 / setu
+ [x] 与chatgpt聊天
+ [x] 天气预报 / 定时提醒
+ [x] 学群友怪话(雾

## 🔋 Instructions

+ 安装`go-cqhttp`框架
+ 替换配置文件`config.yml`以及添加事件过滤器`fliter.json`
+ 获取 src 目录下的功能代码
+ 安装项目依赖 `requirements.txt`
+ 运行`go-cqhttp`机器人框架并运行`main.py`

详细过程请参考: 

1. [基于go-cqhttp框架实现QQ机器人 - 掘金 (juejin.cn)](https://juejin.cn/post/7205935996704636987)
2. [腾讯云部署基于go-cqhttp的qq机器人 - 掘金 (juejin.cn)](https://juejin.cn/post/7205930226445320229)

## 🎮 Description

```
.
├───src
│   ├───api.py            // 机器人功能模块: 用于调用各种指令集
│   ├───main.py           // 主函数: 监听端口并启动功能模块
│   ├───nativeAPI.py      // go-cqhttp原生API: 包括防撤回,发送消息,获取消息
│   ├───config.example.py // 存放敏感信息: API私钥,个人QQ等等
│   ├───requirements.txt  // 依赖库列表
│   ├───struct.json       // mongodb中文档数据结构
│   └───utils
│       ├───cq_code.py    // 包装cqCode以方便操作
│       ├───jieba_word.py // 利用jieba实现关键词提取
│       ├───logger.py     // 日志记录器
│       ├───openai_chat.py// AI对话模块
│       ├───rand_pic.py   // 随机图片模块
│       ├───real_dora.py  // 学群友怪话)
│       └───timing.py     // 定时提醒
│
│   config.yml            // go-cqhttp配置文件参考
└───fliter.json           // 事件过滤器参考: 实现只接收特定群聊和个人的消息,以及撤回类型的消息
```

## 🌺 Special Thanks

[Mrs4s/go-cqhttp: cqhttp的golang实现，轻量、原生跨平台. (github.com)](https://github.com/Mrs4s/go-cqhttp)

