# 🌦️ Command-R 실시간 날씨 연동 에이전트 프로젝트

Ollama의 **Command-R (35B)** 모델을 활용하여, 실시간 날씨 데이터를 분석하고 사용자에게 최적화된 답변을 제공하는 지능형 에이전트입니다.

## 🚀 1. 프로젝트 개요
- **모델**: `command-r`
- **핵심 기능**: 사용자 질문 의도 파악, 실시간 기상 데이터 확보, 개인화된 답변 생성
- **하드웨어**: 96GB RAM (VRAM + RAM 병렬 활용)

---

## 🛠️ 2. 개발 시행착오 및 의사결정 (The Journey)

가장 효율적이고 경제적인 데이터 연동 방식을 찾기 위해 다음과 같은 과정을 거쳤습니다.

1.  **Phase 1: 검색 API (DuckDuckGo(DDG)) 활용 시도**
    - 결과1: 검색 결과가 많은 광고와 함께 나와 포기. 제대로 된 검색 결과를 얻을 수 없었음.
2.  **Phase 2: 직접 크롤링 (BeautifulSoup) 시도**
    - 결과: 기상청 사이트 등의 HTML 구조 변경 및 동적 데이터 로딩 문제로 데이터 추출의 **불안정성** 확인.
3.  **Phase 3: Open-Meteo API 정착 (최종)** 🎯
    - 결과: **완전 무료, API 키 불필요, JSON 포맷의 정제된 데이터** 제공. 모델이 도시의 좌표(위도/경도)를 추론하게 하여 범용성 확보.

---

## 🏗️ 3. 시스템 아키텍처 (Modular Design)

프로젝트는 유지보수와 확장성을 위해 **객체지향(OOP) 구조**로 설계되었습니다.

```text
├── main.py                 # 에이전트 실행 및 UI 루프 (Main Loop)
├── logger_config.py        # 전역 Static Logger 설정 (Logging System)
├── mcp/                    # mcp 서버 모음
│   └── mpc_server.py       # weather tool 실행 코드
├── tools/                  # 기능별 서브 에이전트 모음
│   └── weather.py          # 실시간 날씨 데이터 수집 에이전트
├── inference/              # 추론 엔진
│   └── ollama_inference.py # Ollama API 통신 및 모델 핸들링
├── prompt/                 # 프롬프트
│   ├── main_prompts.py     # 메인 시스템 프롬프트
│   └── weather_prompt.py   # 날씨 데이터 프롬프트
├── util/                   # 시스템 로그 저장 폴더
│   └── logger.py           # 추론 과정 및 에러 기록
├── requirements.txt        # 설치 필요 라이브러리 목록
└── README.md               # 프로젝트 사용 설명서
```
---
## 🖥️ 4. 사용 방법 (Usage)
터미널 실행 후 [질의]: 프롬프트에 질문을 입력하세요.

일반 대화: "너의 이름은 뭐야?" / "오늘 기분 어때?"

실시간 검색: "지금 서울 날씨 어때? 오늘 날짜 기준으로 검색해서 알려줘."

종료: exit 또는 종료 또는 quit 입력