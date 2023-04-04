import requests

locationid = '101270107'
jingwei = '103.90,30.79'
apikey = '12f3889347564f5f94d84c99e20ae08e'
baseUrl = 'https://devapi.qweather.com/v7/'

no_proxy = {
    "http": None,
    "https": None,
}

# 获取地区编号
def getLoc(pos):
    url = 'https://geoapi.qweather.com/v2/city/lookup?location={0}&key={1}'.format(pos,apikey)
    res = requests.get(url,proxies=no_proxy).json()
    if res.get('code')!='200':
        return str(res)
    else:
        locID = res.get('location')[0].get('id')
    return str(locID)

# 大致预报
def briefForecast():
    url = baseUrl + 'weather/3d?location={0}&key={1}'.format(locationid,apikey)
    res = requests.get(url,proxies=no_proxy).json().get('daily')[0]
    tmpMax = res.get('tempMax')
    tmpMin = res.get('tempMin')
    dayText = res.get('textDay')
    nigText = res.get('textNight')
    precip = res.get('precip')
    mes = '🎯  今日天气预报 🐳 \n 降雨: {4}\n 气温: {0}℃ - {1}℃\n 天气: {2}(日 )/ {3}(夜)'.format(
        tmpMin,tmpMax,dayText,nigText,precip
    )
    # print(mes)
    return mes

# 详细预报
def detailForecast(pos=''):
    if pos =='':
        loc = locationid
        pos = '郫都'
    else:
        loc = getLoc(pos)
        print(loc,type(loc))
        if loc.isdigit()==False:
            return loc
    try:
        # 获取实时天气
        url = baseUrl + 'weather/now?location={0}&key={1}'.format(loc,apikey)
        res = requests.get(url,proxies=no_proxy).json().get('now')
        mes = []
        mes.append('当前：{0}℃ / {1}'.format(res['temp'],res['text']));
        # 获取逐小时预报
        url = baseUrl + 'weather/24h?location={0}&key={1}'.format(loc,apikey)
        resJson = requests.get(url,proxies=no_proxy).json()
        res = resJson.get('hourly')
        for i in range(6):
            tmpTime = res[i].get('fxTime').split('T')
            tmpTime = tmpTime[1].split('+')[0]
            temp = res[i].get('temp')
            text = res[i].get('text')
            mes.append('{0}  {1}℃ / {2}'.format(tmpTime,temp,text))
        updateTime = resJson.get('updateTime')[11:16] # 取出具体时间
        return '☁️  逐小时天气预报 🌞\n' + '地区:  {0}\n'.format(pos) + \
            '\n'.join(mes) + '\n更新时间: ' + updateTime
    except Exception as e:
        return str(e)

# 天气预警
# https://devapi.qweather.com/v7/warning/now?location=101270107&key=12f3889347564f5f94d84c99e20ae08e

def warning():
    url = baseUrl + 'warning/now?location={0}&key={1}'.format(locationid,apikey)
    # print(url)
    res = requests.get(url,proxies=no_proxy).json().get('warning')
    if len(res)==0:
        return 'No Warning'
    return res[0].get('text')