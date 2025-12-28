
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# 1. 현재 파일(mcp_server.py)의 위치를 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 한 단계 위 폴더(프로젝트 루트) 경로를 계산합니다.
project_root = os.path.dirname(current_dir)

# 3. 파이썬이 모듈을 찾는 경로(sys.path)에 프로젝트 루트를 추가합니다.
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from mcp.server.fastmcp import FastMCP
from tools.weather import WeatherAgent
from inference.ollama_inference import OllamaInference
from util.logger import ChobigLogger

# 1. MCP 서버 객체 생성
mcp = FastMCP("Chobig_Super_Server")
log = ChobigLogger.get_logger()
inference = OllamaInference("command-r")


# 2. 날씨 도구 등록
@mcp.tool()
def fetch_local_weather(search_keyword) -> str:
    """
    지정된 도시의 실시간 날씨 정보를 weather 엔진으로 분석하여 리턴합니다.
    """
    log.info(f"MCP 요청 수신: {search_keyword} 조회 중...")

    try:
        # 기존에 만든 WeatherAgent 호출
        agent = WeatherAgent(inference)
        result = agent.run(search_keyword)
        return f"{result}"
    except Exception as e:
        return f"날씨 조회 중 에러 발생: {str(e)}"


if __name__ == "__main__":
    log.info("weather mcp를 가동합니다. 슈우웅~")
    # MCP 서버 가동 (Stdio 방식)
    mcp.run()