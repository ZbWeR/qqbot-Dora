<h1 align="center">🤖 基于go-cqhttp的qqBot 🧊</h1>

### 🎯 已实现功能

+ [x] 自动复读
+ [x] 随机图片/setu
+ [x] 群聊防撤回
+ [x] 与chatgpt聊天
+ [x] 天气预报 
+ [x] 定时提醒

### 🔋 使用说明

+ 安装`go-cqhttp`框架:链接在本文末尾
+ 替换配置文件`config.yml`以及添加事件过滤器`fliter.json`
+ 运行机器人并运行`main.py`

详细过程请参考: 

1. [基于go-cqhttp框架实现QQ机器人 - 掘金 (juejin.cn)](https://juejin.cn/post/7205935996704636987)
2. [腾讯云部署基于go-cqhttp的qq机器人 - 掘金 (juejin.cn)](https://juejin.cn/post/7205930226445320229)

### 📝 文件描述

```
.
├───src
│   ├───api.py           // 机器人功能模块
│   ├───main.py          // 主函数: 监听端口并调用功能模块
│   ├───weather.py       // 与天气预报相关的外部API
│   ├───nativeAPI.py     // go-cqhttp原生API
│   ├───openChat.py      // AI对话模块
│   ├───randPic.py       // 随机图片模块
│   ├───openChat.py      // AI对话模块
│   └───timing.py        // 定时提醒
│   config.yml           // go-cqhttp配置文件参考
└───fliter.json          // 事件过滤器参考: 实现只接收特定群聊和个人的消息,以及撤回类型的消息
```

### ❤ 特别鸣谢

[Mrs4s/go-cqhttp: cqhttp的golang实现，轻量、原生跨平台. (github.com)](https://github.com/Mrs4s/go-cqhttp)
