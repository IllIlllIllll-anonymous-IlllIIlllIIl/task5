import requests
import os

class AmapGeocoder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://restapi.amap.com/v3/geocode/geo"
    
    def get_coordinates(self, city_name):
        """
        获取城市经纬度
        参数:
            city_name (str): 城市名称
        返回:
            tuple: (经度, 纬度) 或 None如果未能获取到结果
        """
        params = {
            "key": self.api_key,
            "address": city_name
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != '1':
                print(f"请求失败：{data.get('info', '未知错误')} - {data.get('infocode', '')}")
                return None
            
            geocodes = data.get('geocodes', [])
            if not geocodes:
                print("未找到相关结果")
                return None
                
            location = geocodes[0].get('location')
            if not location:
                print("位置信息无效")
                return None
                
            try:
                longitude, latitude = map(float, location.split(','))
                return (longitude, latitude)
            except ValueError:
                print("经纬度格式错误")
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"网络请求异常：{str(e)}")
        except Exception as e:
            print(f"处理响应时发生异常：{str(e)}")
        
        return None


if __name__ == "__main__":
    # 在高德开放平台获取API Key
    API_KEY = os.getenv('gaode_api') # 系统下配置好高德api_key，那玩意可能按流量收费
    
    geocoder = AmapGeocoder(API_KEY)
    
    while True:
        city = input("请输入要查询的城市名称（输入q退出）: ").strip()
        if city.lower() == 'q':
            break
            
        if not city:
            print("输入不能为空，请重新输入")
            continue
            
        coordinates = geocoder.get_coordinates(city)
        
        if coordinates:
            print(f"经度：{coordinates[0]}, 纬度：{coordinates[1]}")
        else:
            print("未能获取到有效的经纬度，请尝试更完整的城市名称（如：'北京市'）")