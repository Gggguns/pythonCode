import requests
import json
import time
import textToSpeech
import GPS
import threading
from util import JsonUtil
from radarScanning import obstacleDetection
from radarActive import activatedRadar
# 此处填写您在控制台-应用管理-创建应用后获取的AK
ak = "0AFgwYGcQKt4UUcwxtPqu1YjBfD7gbda"

# 向百度API发送请求
def sendRequest(uri, params):
    host = "http://api.map.baidu.com"
    query_str = "&".join([f"{key}={value}" for key, value in params.items()])
    url = host + uri + "?" + query_str
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

# 地址转经纬度
def addressTranslationLatitudeAndLongitude(address):
    uri = "/geocoding/v3"
    # 这里的 ak 变量应该在某个地方定义，确保它是可用的
    params = {
        "address": address,
        "output": "json",
        "ak": ak,
        "callback": "showLocation"
    }
    curl_result = sendRequest(uri, params)
    # #Debug
    # print(curl_result)
    json_str = curl_result[curl_result.find('(')+1:curl_result.find(')')]
    j = json.loads(json_str)
    lng = j["result"]["location"]["lng"]
    lat = j["result"]["location"]["lat"]
    # #Debug
    # print(f"lng: {lng}")
    # print(f"lat: {lat}")
    return lat, lng
    
# 获取指引
def getGuidance(origin, destination):
    # #Debug
    # print("Debug")
    # print("origin")
    # print(origin)
    # print("destination")
    # print(destination)
    uri = "/directionlite/v1/walking"
    # 这里的 ak 变量应该在某个地方定义，确保它是可用的
    params = {
        "origin": origin,
        "destination": destination,
        "output": "json",
        "ak": ak
    }
    response = sendRequest(uri, params)
    return response

# 从Json中提取指引信息
def extractInstrctionFromJson(json_str):
    data = json.loads(json_str)
    if "result" in data and "routes" in data["result"]:
        routes = data["result"]["routes"]
        for route in routes:
            if "steps" in route:
                steps = route["steps"]
                for step in steps:
                    if "instruction" in step:
                        instruction = step["instruction"]
                        instruction = JsonUtil.removeLabel(instruction)
                        print("雷达扫描")
                        #扫描前方是否有障碍物
                        obstacleDetection()
                        time.sleep(1)
                        #Debug
                        print(instruction)
                        #播报提示
                        if instruction is not None:
                            textToSpeech.textToSpeechPlayback(instruction)
                        time.sleep(1);
    else:
        print("No routes or steps found in the JSON data.")
    
# 路径规划
def routePlanning(des_lat_lon):
    # 获取当前位置经纬度
    ori_lat_lon = GPS.get_lat_lon()
    if ori_lat_lon is None or len(ori_lat_lon) < 2:
        print("获取当前位置经纬度失败，可能是函数 get_lat_lon 返回 None 或数据不完整")
        return
    if des_lat_lon is None or len(des_lat_lon) < 2:
        print("目的地经纬度转换失败，可能是函数 addressTranslationLatitudeAndLongitude 返回 None 或数据不完整")
        return
        
    # 获取路径规划信息
    guidance_result = getGuidance(JsonUtil.float_to_string(ori_lat_lon[0], ori_lat_lon[1]),
                                    JsonUtil.float_to_string(des_lat_lon[0], des_lat_lon[1]))
    # 提取行走指引信息
    if guidance_result:
        extractInstrctionFromJson(guidance_result)
        #Debug
        time.sleep(2)
    
def _navigationPrompt(address):
    time.sleep(10)
    #目的地地址转经纬度
    des_lat_lon = addressTranslationLatitudeAndLongitude(address)
    #获取周围信息提供提供提示
    while True:
        #路线规划
        routePlanning(des_lat_lon)
        time.sleep(1)

#导航提示
def navigationPrompt(address):
    #创建线程
    rthread = threading.Thread(target=_navigationPrompt,kwargs={"address": address})
    rthread.start()
    #启动雷达
    activatedRadar()
    

#示例
if __name__ == "__main__":
     #Path.addressTranslationLatitudeAndLongitude()
    guidance_result = getGuidance()
    if guidance_result:
        extractInstrctionFromJson(guidance_result)