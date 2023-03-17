import requests

locationid = '101270107'
jingwei = '103.90,30.79'
apikey = '12f3889347564f5f94d84c99e20ae08e'
baseUrl = 'https://devapi.qweather.com/v7/'

def getLoc(pos):
    url = 'https://geoapi.qweather.com/v2/city/lookup?location={0}&key={1}'.format(pos,apikey)
    res = requests.get(url).json()
    if res.get('code')!='200':
        return str(res)
    else:
        locID = res.get('location')[0].get('id')
    return str(locID)

# 大致预报
def briefForecast():
    url = baseUrl + 'weather/3d?location={0}&key={1}'.format(locationid,apikey)
    res = requests.get(url).json().get('daily')[0]
    tmpMax = res.get('tempMax')
    tmpMin = res.get('tempMin')
    dayText = res.get('textDay')
    nigText = res.get('textNight')
    precip = res.get('precip')
    mes = '🎯  今日天气预报 🐳 \n 降雨:{4}\n 气温: {0}℃ - {1}℃\n 天气: {2}(日 )/ {3}(夜)'.format(
        tmpMin,tmpMax,dayText,nigText,precip
    )
    print(mes)
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
    url = baseUrl + 'weather/24h?location={0}&key={1}'.format(loc,apikey)
    res = requests.get(url).json().get('hourly')
    mes = []
    for i in range(6):
        tmpTime = res[i].get('fxTime').split('T')
        tmpTime = tmpTime[1].split('+')[0]
        temp = res[i].get('temp')
        text = res[i].get('text')
        mes.append('{0}  {1}℃ / {2}'.format(tmpTime,temp,text))
    return '☁️  逐小时天气预报 🌞\n' + '地区:  {0}\n'.format(pos) + '\n'.join(mes)

# 天气预警
def warning():
    url = baseUrl + 'warning/now?location={0}&key={1}'.format(locationid,apikey)
    # print(url)
    res = requests.get(url).json().get('warning')
    if len(res)==0:
        return ''
    return res[0].get('text')