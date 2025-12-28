import logging
import os


class ChobigLogger:
    # 클래스 변수로 로거 설정 (Static 효과)
    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            # 로거 객체 생성
            cls._logger = logging.getLogger("ChobigAgent")
            cls._logger.setLevel(logging.INFO)

            # 포맷 설정 (시간 [레벨] 메시지)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

            # 1. 파일 핸들러 (로그를 파일에 저장)
            file_handler = logging.FileHandler("logs/agent_process.log", encoding='utf-8')
            file_handler.setFormatter(formatter)

            # 2. 콘솔 핸들러 (화면에도 찍고 싶을 때)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            cls._logger.addHandler(file_handler)
            cls._logger.addHandler(stream_handler)

        return cls._logger