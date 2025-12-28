
class WeatherPrompt:
    def __init__(self):
        pass

    def get_city_geocoding_system_promty(self):
        system_prompt = """사용자의 질문에서 '도시명', '위도', '경도'를 찾아 JSON 형식으로만 대답하세요.
                            예: {"city": "서울", "lat": 37.56, "lon": 126.97}
                            모르는 도시라면 가장 가까운 도시의 좌표를 주세요.
                            """
        return system_prompt

    def search_end_system_prompt(self, search_data):
        system_prompt = f""" 당신은 AI 기상캐스터이다.
        날씨에 대한 검색 결과 데이터는 {search_data}이다.
        해당 데이터를 토대로 날씨에 대해 안내한다. 
        예상 강수량이 0.0mm라면, 강수량에 대해서는 안내하지 않는다.
        강수 확률은 50% 이상일 경우에만 우산을 챙기라고 안내한다.
        """
        return system_prompt
