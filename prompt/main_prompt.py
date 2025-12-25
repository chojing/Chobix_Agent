from datetime import datetime


class MainPrompt:
    def __init__(self):
        pass

    def start_system_prompt(self):
        today = datetime.now().strftime("%Y-%m-%d")
        system_prompt = f"""당신은 초빅스 라는 이름의 AI 비서 입니다. 오늘 날짜는 {today}입니다.
            반드시 사용자의 질문에 답하기 위해 최신 정보가 필요하다면 'SEARCH: 검색어'라고 출력하세요
            날씨와 관련된 질문이라면, 맨 앞에 [날씨] 를 출력하세요.
            """
        return system_prompt

    def end_system_prompt(self, search_data):
        system_prompt = f"""검색결과 : {search_data}.
                    """
        return system_prompt