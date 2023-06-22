import requests
import random
from utils.logger import logger
# from logger import logger

apiArr = [
    'https://api.gmit.vip/Api/DmImg?format=json',
    'https://api.lolicon.app/setu/v2',
    'https://sex.nyan.xyz/api/v2/'
    ]

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

def get_normal_pic():
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
        logger.error(f"普通图片接口出错:{e}")

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
        logger.error(f"色图接口出错:{e}")
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
        logger.error(f"色图接口出错:{e}")
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
        logger.error(f"摸鱼接口出错:{e}")
        return '⚠️接口访问出错啦!'