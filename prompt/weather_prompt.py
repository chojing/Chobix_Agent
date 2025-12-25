
class WeatherPrompt:
    def __init__(self):
        pass

    def get_city_geocoding_system_promty(self):
        system_prompt = """사용자의 질문에서 '도시명', '위도', '경도'를 찾아 JSON 형식으로만 대답하세요.
                            예: {"city": "서울", "lat": 37.56, "lon": 126.97}
                            모르는 도시라면 가장 가까운 다른 한국의 도시 좌표를 주세요.
                            """
        return system_prompt