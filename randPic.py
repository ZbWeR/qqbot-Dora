import requests
import random

apiArr = [
    'https://api.gmit.vip/Api/DmImg?format=json',
    'https://api.lolicon.app/setu/v2',
    'https://sex.nyan.xyz/api/v2/'
    ]

# 正常图片
def normal():
    url = 'https://api.gmit.vip/Api/DmImg?format=json'
    res = requests.get(url).json()
    code = res.get('code')
    if code != '200':
        return '⚠️访问出错啦!\n' + 'Status Code: '+code
    resUrl = res.get('data')['url']
    return '[CQ:image,file={0},subType=0,url={1}]'.format('fbekjqdnl1.image',resUrl)

# 生成随机字符串,用于发送CQ码
def generate_random_str(randomlength=8):
    random_str =''
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str

def setu(message):
    arr = message.split(' ')
    if len(arr)==1:
        mes='nil'
        aid=None
    elif len(arr)==2:
        mes = 'nil' if arr[1].isdigit() else arr[1]
        aid = arr[1] if arr[1].isdigit() else None
    elif len(arr)==3:
        mes = arr[2] if arr[1].isdigit() else arr[1]
        aid = arr[1] if arr[1].isdigit() else arr[2]
    tmpNum = random.randint(1,2)
    if tmpNum==1:
        return setu1(mes,aid)
    elif tmpNum==2:
        return setu2(mes,aid)

def setu1(mes='nil',aid=None):
    # print(mes)
    if aid==None:
        url = 'https://sex.nyan.xyz/api/v2/?tag=' + mes
    else:
        url = 'https://sex.nyan.xyz/api/v2/?tag={0}&author_uuid={1}'.format(mes,aid)
    res = requests.get(url).json()
    resUrl = res.get('data')
    if resUrl== None:
        return '不存在该tag的数据哦~'
    return '画师uid:{2}\n[CQ:image,file={0},subType=0,url={1}]'.format(
        generate_random_str() + '.image',
        resUrl[0]['url'],
        resUrl[0]['author_uid']
        )

def setu2(mes='ni',aid=None):
    # print(mes)
    if aid==None:
        url = 'https://api.lolicon.app/setu/v2?tag=' + mes
    else:
        url = 'https://api.lolicon.app/setu/v2?tag={0}&uid={1}'.format(mes,aid)
    res = requests.get(url).json()
    resUrl = res.get('data')
    
    if resUrl== None or len(resUrl)==0:
        return '不存在该tag的数据哦~'
    return '画师uid:{2}\n[CQ:image,file={0},subType=0,url={1}]'.format(
        generate_random_str() + '.image',
        resUrl[0]['urls']['original'],
        resUrl[0]['uid']
        )