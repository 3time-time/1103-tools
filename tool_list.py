"""
66c5be3d1c904442bb04f14f1eaca702
jt759g9ke2.re.qweatherapi.com
https://abcxyz.qweatherapi.com/weather/v1/current/39.92/116.41
实时天气：GET /weather/v1/current/{latitude}/{longitude}
# url = r"https://jt759g9ke2.re.qweatherapi.com/weather/v1/current/39.92/116.41"
"""
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field


base_url = r"https://jt759g9ke2.re.qweatherapi.com"
headers = {
        "X-QW-Api-Key": "66c5be3d1c904442bb04f14f1eaca702"   
    }

class Weather(BaseModel):
    city_name: str = Field(description="城市名")

def get_geo(city):
    url = base_url + f"/geo/v2/city/lookup?location={city}"
    response = requests.get(url, headers=headers, timeout=10)
    # print(response.status_code)
    # print(response.text)
    data = response.json()['location'][0]
    lat = round(float(data['lat']), 2)
    lon = round(float(data['lon']),2)
    # print(city, lat, lon)
    return lat,lon
@tool(args_schema=Weather)
def get_weather(city_name: str) -> str:
    """查询指定城市的当前天气"""
    lat, lon = get_geo(city_name)
    url = base_url + f"/weather/v1/current/{lat}/{lon}"
    response2 = requests.get(url, headers=headers, timeout=10)
    data = response2.json()
    condition = data['condition']['text']
    temp = data['temperature']['value']
    temperature = round(temp)
    # print(city_name, condition, temperature)
    return f"查询{city_name}的天气为{condition}, 温度为{temperature}℃。"

def tool_list():
    return [get_weather]