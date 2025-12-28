import requests
import re
from inference.ollama_inference import OllamaInference
from prompt.weather_prompt import WeatherPrompt
import json
from util.logger import ChobigLogger

log = ChobigLogger.get_logger()

class WeatherAgent:
    def __init__(self, ollama_inference:OllamaInference):
        self.weather_prompt:WeatherPrompt = WeatherPrompt()
        self.ollama_inference:OllamaInference = ollama_inference

    def run(self, content):
        #도시 위치 정보 (위도, 경도) 가져 오기
        # content : 2025-12-25 서울 날씨
        # output : {"city": "서울", "lat": 37.56, "lon": 126.97}
        system_prompt = self.weather_prompt.get_city_geocoding_system_promty()
        output = self.ollama_inference.inference(system_prompt, content)

        json_string = re.search(r'\{.*\}', output, re.DOTALL).group()
        data = json.loads(json_string)

        #api를 이용하여 날씨 정보 획득
        weather_data = self.get_full_weather_api(data["lat"], data["lon"], data["city"])

        return weather_data

    def get_full_weather_api(self, lat, lon, city_name):
        print("글로벌 기상 서버(Open-Meteo)에서 풀옵션 데이터 추출 중...")

        # 서울 좌표 + 필요한 옵션들 (최고/최저 기온, 강수 확률, 강수량 등)
        # daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max 옵션 추가
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,rain_sum"
            f"&timezone=Asia%2FSeoul"
        )

        try:
            response = requests.get(url)
            data = response.json()

            # 1. 현재 날씨
            current = data['current_weather']
            curr_temp = current['temperature']

            # 2. 오늘 하루 요약 (daily 데이터의 첫 번째 항목이 오늘임)
            daily = data['daily']
            max_temp = daily['temperature_2m_max'][0]
            min_temp = daily['temperature_2m_min'][0]
            rain_prob = daily['precipitation_probability_max'][0]  # 강수 확률 (%)
            rain_sum = daily['rain_sum'][0]  # 예상 강수량 (mm)

            # 비 유무 판단
            is_raining = "있음" if rain_prob > 20 or rain_sum > 0 else "없음"

            weather_fact = (
                f"[{city_name} 실시간 기상 리포트]\n"
                f"- 현재 기온: {curr_temp}°C\n"
                f"- 오늘 최고 기온: {max_temp}°C\n"
                f"- 오늘 최저 기온: {min_temp}°C\n"
                f"- 강수 확률: {rain_prob}%\n"
                f"- 비 소식 유무: {is_raining} (예상 강수량: {rain_sum}mm)"
            )
            return weather_fact
        except Exception as e:
            return f"데이터 추출 실패: {e}"

