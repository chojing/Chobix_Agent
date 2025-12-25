from inference.ollama_inference import OllamaInference
from prompt.main_prompt import MainPrompt
from tools.weather import WeatherAgent

from util.logger import ChobigLogger

log = ChobigLogger.get_logger()

class Main:
    def __init__(self):
        self.model_name = "command-r"
        self.main_prompt:MainPrompt = MainPrompt()
        self.ollama_inference:OllamaInference = OllamaInference(self.model_name)

    def run_command_r_agent(self, user_question):
        system_prompt = self.main_prompt.start_system_prompt()

        # 1. 의도 판단 단계
        content = self.ollama_inference.inference(system_prompt, user_question)
        log.info(f"1 판단 단계 결과 : {content}")

        # 2. 검색 실행 여부 확인
        if "SEARCH:" in content:
            # SEARCH: 뒷부분만 깔끔하게 따내기
            search_query = content.split("SEARCH:")[1].strip().split('\n')[0]
            if "[날씨]" in content:
                weather_agent = WeatherAgent(self.ollama_inference)
                search_query = weather_agent.run(search_query)
                log.info(f"실시간 날씨 정보 : {search_query}")

            # 3. 검색 결과를 들고 다시 답변 생성
            system_prompt = self.main_prompt.end_system_prompt(search_query)
            log.info(f"검색결과 system prompt : {system_prompt}")
            final_res = self.ollama_inference.inference(system_prompt, user_question)
            return final_res
        return content


if __name__ == "__main__":
    # 가동!
    print(f"📡 Command-R(35B) 에이전트 대기 중... (VRAM + RAM 활용 모드)")
    main = Main()

    while True:
        user_input = input("[질의]: ")

        if user_input.lower() in ['종료', 'exit', 'quit']:
            log.info("종료합니다.")
            #print("종료합니다.")
            break

        if not user_input.strip():
            continue

        try:
            #에이전트에게 질의
            #q = "지금 서울 날씨 어때? 오늘 날짜 기준으로 검색해서 알려줘."
            ret = main.run_command_r_agent(user_input)
            print(f"\n[초빅스의 답변]:\n {ret} ")

        except Exception as e:
            print(f"루프 중 오류 발생! {e}")
        finally:
            print("완료!")