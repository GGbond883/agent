import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4-turbo-preview"  # 或 "gpt-3.5-turbo"
    TEMPERATURE = 0.7

    # API 配置
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # 用于搜索

    # Agent 配置
    MAX_ITERATIONS = 3  # 最大重试次数
    TIMEOUT_SECONDS = 30