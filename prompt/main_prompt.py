from datetime import datetime


class MainPrompt:
    def __init__(self):
        pass

    def start_system_prompt(self):
        today = datetime.now().strftime("%Y-%m-%d")
        system_prompt = f"""당신은 초빅스 라는 이름의 AI 비서 입니다. 
            오늘 날짜는 {today}입니다.
            해당 질의의 유형이 어떤 유형인지 판단하여 아래의 구분 내에서 하나만 답하시오.
            [구분]
            1. 검색
            2. 날씨
            3. 일상대화
            
            예시1) 오늘 뉴스 알려줘
            답변1) [검색] : 뉴스 키워드
            
            예시2) 오늘 날씨 알려줘
            답변2) [날씨] : 날짜 도시 날씨 알려줘.
            
            예시3) 안녕?
            답변3) [일상대화] : 일상대화 답변
            """
        return system_prompt

    def end_system_prompt(self, search_data):
        system_prompt = f"""검색결과 : {search_data}.
                    """
        return system_prompt