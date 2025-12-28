from inference.ollama_inference import OllamaInference
from prompt.main_prompt import MainPrompt
from prompt.weather_prompt import WeatherPrompt
from tools.weather import WeatherAgent
import asyncio
from mcp_servers import ClientSession, StdioServerParameters
from mcp_servers.client.stdio import stdio_client
import re
from util.logger import ChobigLogger

log = ChobigLogger.get_logger()

class Main:
    def __init__(self):
        self.model_name = "command-r"
        self.main_prompt:MainPrompt = MainPrompt()
        self.weather_prompt:WeatherPrompt = WeatherPrompt()
        self.ollama_inference:OllamaInference = OllamaInference(self.model_name)

        #mcp_servers 위치 지정
        self.weather_mcp = StdioServerParameters(
            command="python",
            args=["mcp_servers/mcp_server.py"],
            env=None
        )

    async def main_async(self, user_question):
        system_prompt = self.main_prompt.start_system_prompt()
        log.info("main_async 진입 완료. system prompt get.")
        # 1. 의도 판단 단계
        content = self.ollama_inference.inference(system_prompt, user_question)
        log.info(f"1 판단 단계 결과 : {content}")

        # 2. 검색 실행 여부 확인
        if "[날씨]" in content:
            match = re.search(r"\[날씨\]\s*(.*)", content)
            if match:
                search_query = match.group(1).strip()
                weather_info = await self.run_mcp(search_query)
                log.info(f"날씨 분석 결과 : {weather_info}")
                # 3. 검색 결과를 들고 다시 답변 생성
                system_prompt = self.weather_prompt.search_end_system_prompt(weather_info.content[0].text)
                log.info(f"검색결과 system prompt : {system_prompt}")
                content = self.ollama_inference.inference(system_prompt, user_question)
        return content


    async def run_mcp(self, search_keyword):
        log.info("초빅스 async 가동!")

        async with stdio_client(self.weather_mcp) as (read, write):
            async with ClientSession(read,write) as session:
                # 서버 초기화
                await session.initialize()
                log.info("MCP 서버 연결 성공!")

                log.info(f"search keyword : {search_keyword}")
                result = await session.call_tool("fetch_local_weather", {"search_keyword":search_keyword})

                return result

    # def run_agent_old(self, user_question):
    #     system_prompt = self.main_prompt.start_system_prompt()
    #
    #     # 1. 의도 판단 단계
    #     content = self.ollama_inference.inference(system_prompt, user_question)
    #     log.info(f"1 판단 단계 결과 : {content}")
    #
    #     # 2. 검색 실행 여부 확인
    #     if "SEARCH:" in content:
    #         # SEARCH: 뒷부분만 깔끔하게 따내기
    #         search_query = content.split("SEARCH:")[1].strip().split('\n')[0]
    #         if "[날씨]" in content:
    #             weather_agent = WeatherAgent(self.ollama_inference)
    #             search_query = weather_agent.run(search_query)
    #             log.info(f"실시간 날씨 정보 : {search_query}")
    #
    #         # 3. 검색 결과를 들고 다시 답변 생성
    #         system_prompt = self.main_prompt.end_system_prompt(search_query)
    #         log.info(f"검색결과 system prompt : {system_prompt}")
    #         final_res = self.ollama_inference.inference(system_prompt, user_question)
    #         return final_res
    #     return content


if __name__ == "__main__":
    # 가동!
    print(f"📡 Command-R(35B) 에이전트 대기 중... (VRAM + RAM 활용 모드)")
    main = Main()

    async def run_chat():
        while True:
            user_input = input("[질의]: ")

            if user_input.lower() in ['종료', 'exit', 'quit']:
                log.info("종료합니다.")
                break

            if not user_input.strip():
                continue

            try:
                #에이전트에게 질의
                user_input = "지금 서울 날씨 어때? 오늘 날짜 기준으로 검색해서 알려줘."
                ret = await main.main_async(user_input)
                print(f"\n[초빅스의 답변]:\n {ret} ")

            except Exception as e:
                print(f"루프 중 오류 발생! {e}")
            finally:
                print("완료!")

asyncio.run(run_chat())