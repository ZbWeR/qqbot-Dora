import requests
import random
from utils.logger import dora_log
# from dora_log import dora_log

def get_setu(num):
    """
    获取色图的主函数
    Args:
        message: str, 包含用户想要图片的数量
    Returns:
        str, 包含图片的CQ码
    """
    if random.random() <= 0.5:
        return get_sexy_pic_1(num)
    else:
        return get_sexy_pic_2(num)

def get_pic():
    if random.random() <= 0.5:
        return get_normal_pic_1()
    else:
        return get_normal_pic_2()

def generate_random_str(randomlength=8):
    """
    生成一个随机字符串
    Args:
        randomlength: int, 字符串的长度
    Returns:
        random_str: str, 随机字符串
    """
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    random_str = ''.join([base_str[random.randint(0, length)] for i in range(randomlength)])
    return random_str

def get_normal_pic_1():
    """
    获取正常的动漫图片
    """
    url = [
        'https://api.gmit.vip/Api/DmImgS?format=json',
        'https://api.gmit.vip/Api/DmImg?format=json'
    ]
    try:
        res = requests.get(url[random.randint(0,len(url)-1)]).json()
        code = res.get('code')
        if code == '200':
            resUrl = res.get('data')['url']
            return f'[CQ:image,file={generate_random_str()}.image,subType=0,url={resUrl}]'
        return '⚠️访问出错啦!\n' + 'Status Code: '+code
    except Exception as e:
        dora_log.error(f"普通图片接口出错:{e}")

def get_normal_pic_2():
    url = 'https://api.r10086.com/%E6%A8%B1%E9%81%93%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87api%E6%8E%A5%E5%8F%A3.php?%E8%87%AA%E9%80%82%E5%BA%94%E5%9B%BE%E7%89%87%E7%B3%BB%E5%88%97=%E5%8E%9F%E7%A5%9E'
    baseurl = 'https://api.r10086.com/图包webp/原神横屏系列1/'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'
    }
    try:    
        res = requests.get(url,headers=headers)
        # 重定向历史中找到目标url
        loc = res.history[0].headers.get('Location')
        usefulloc = loc[loc.find('wallhaven'):]
        return f"[CQ:image,file={generate_random_str()}.image,subType=0,url={baseurl+usefulloc}]"
    except Exception as e:
        dora_log.error(f"普通图片接口出错:{e}")
        return '⚠️接口访问出错啦!'

def get_sexy_pic_1(num=1):
    """
    获取色图
    Args:
        num: int,图片的数量
    Returns:
        cont: str, 包含图片信息的CQ字符串
    """
    url = f"https://api.lolicon.app/setu/v2?num={num}"
    try:
        res = requests.get(url).json()
        res_url = res.get('data')
        cont = [f"[CQ:image,file={generate_random_str()}.image,subType=0,url={item['urls']['original']}]" for item in res_url]
        return cont
    except Exception as e:
        dora_log.error(f"色图接口出错:{e}")
        return '⚠️接口访问出错啦!'

def get_sexy_pic_2(num=1):
    sorts = ['setu','pixiv','jitsu']
    url = f"https://moe.anosu.top/api?type=json&sort={sorts[random.randint(0,len(sorts)-1)]}&num={num}"
    try:
        res = requests.get(url).json()
        res_url = res.get('pics')
        cont = [f"[CQ:image,file={generate_random_str()}.image,subType=0,url={item}]"for item in res_url]
        return cont
    except Exception as e:
        dora_log.error(f"色图接口出错:{e}")
        return '⚠️接口访问出错啦!'

def moyu_pic():
    """
    获取摸鱼人日历
    """
    url = 'https://api.j4u.ink/v1/store/other/proxy/remote/moyu.json'
    try:
        res = requests.get(url).json()
        resUrl = res["data"]["moyu_url"]
        return f'[CQ:image,file={generate_random_str()}.image,subType=0,url={resUrl}]'
    except Exception as e:
        dora_log.error(f"摸鱼接口出错:{e}")
        return '⚠️接口访问出错啦!'