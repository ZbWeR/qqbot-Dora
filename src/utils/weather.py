import requests

from config import WEATHER_API_KEY

LOCATION_ID = '101270107'
# BASE_URL = 'https://devapi.qweather.com/v7/'
BASE_URL = 'https://api.qweather.com/v7/'
NO_PROXY = {
    "http": None,
    "https": None,
}

def get_location_id(pos):
    """
    获取地区编号

    Args:
        pos: str, 地区或城市名称
    Returns:
        location_id: str, 对应的地区编号
    """
    url = f'https://geoapi.qweather.com/v2/city/lookup?location={pos}&key={WEATHER_API_KEY}'
    res = requests.get(url,proxies=NO_PROXY).json()
    if res.get('code')!='200':
        return str(res)
    else:
        location_id = res.get('location')[0].get('id')
    return str(location_id)

def brief_forecast():
    """
    简洁版本的每日天气预报

    Returns:
        str, 简短的天气预报
    """
    url = f'{BASE_URL}weather/3d?location={LOCATION_ID}&key={WEATHER_API_KEY}'
    res = requests.get(url,proxies=NO_PROXY).json().get('daily')[0]
    tmpMax = res.get('tempMax')
    tmpMin = res.get('tempMin')
    dayText = res.get('textDay')
    nigText = res.get('textNight')
    precip = res.get('precip')
    return f'🎯  今日天气预报 🐳 \n 降雨: {precip}\n 气温: {tmpMin}℃ - {tmpMax}℃\n 天气: {dayText}(日 )/ {nigText}(夜)'
    # TODO 异常处理

def detail_forecast(pos=''):
    """
    获取 6 小时内的详细天气预报

    Args:
        pos: str, 地区或城市名称
    Returns:
        str, 天气预报文案
    """
    if pos =='':
        loc = LOCATION_ID
        pos = '郫都'
    else:
        loc = get_location_id(pos)
        if not loc.isdigit():
            return loc
    try:
        # 获取实时天气
        url = f'{BASE_URL}weather/now?location={loc}&key={WEATHER_API_KEY}'
        res = requests.get(url,proxies=NO_PROXY).json().get('now')
        mes = []
        mes.append(f'当前：: {res["temp"]}℃ / {res["text"]}')
        # 获取逐小时预报
        url = f'{BASE_URL}weather/24h?location={loc}&key={WEATHER_API_KEY}'
        resJson = requests.get(url,proxies=NO_PROXY).json()
        res = resJson.get('hourly')
        for i in range(6):
            tmpTime = res[i].get('fxTime').split('T')
            tmpTime = tmpTime[1].split('+')[0]
            temp = res[i].get('temp')
            text = res[i].get('text')
            mes.append(f'{tmpTime}  {temp}℃ / {text}')
        updateTime = resJson.get('updateTime')[11:16] # 取出具体时间
        return f'☁️  逐小时天气预报 🌞\n地区:  {pos}\n' + \
            '\n'.join(mes) + '\n更新时间: ' + updateTime
    except Exception as e:
        return str(e)

def warning():
    """
    获取天气预警信息
    """
    url = f'{BASE_URL}warning/now?location={LOCATION_ID}&key={WEATHER_API_KEY}'
    res = requests.get(url,proxies=NO_PROXY).json().get('warning')
    if not res:
        return 'No Warning'
    return res[0].get('text')
