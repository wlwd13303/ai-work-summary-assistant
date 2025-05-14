import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "智汇周报"
    APP_VERSION: str = "0.0.1"
    APP_PREFIX: str = "/api/v1"

    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    DEEPSEEK_MODEL_NAME: str = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")

    # 原模型配置（保留但不使用）
    MODEL_NAME: str = os.getenv("MODEL_NAME", "THUDM/chatglm3-6b")
    DEVICE: str = os.getenv("DEVICE", "cpu")

    class Config:
        env_file = ".env"


settings = Settings()