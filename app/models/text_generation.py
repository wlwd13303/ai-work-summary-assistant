import logging

import requests

from app.config import settings

logger = logging.getLogger(__name__)


class TextGenerationModel:
    def __init__(self):
        self.initialized = True
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL

    def initialize(self):
        """初始化API配置"""
        if not self.api_key:
            logger.error("未设置DeepSeek API密钥")
            return False
        self.initialized = True
        logger.info("DeepSeek API初始化成功")
        return True

    def generate(self, input_text, max_length=4096):
        """生成文本"""
        if not self.initialized:
            self.initialize()

        try:
            # 为周报生成构建提示词
            prompt = f"""请根据以下工作内容，生成一份结构良好、表达专业的工作周报：
                    {input_text}
                    请生成包含以下部分的周报：
                    1. 本周工作内容和成果
                    2. 下周工作计划
                    3. 工作中遇到的问题和解决方案（如果有）
                    4. 工作心得（如果有）
                    """

            # 构建请求体
            payload = {
                "model": settings.DEEPSEEK_MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": max_length,
            }

            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

            response = requests.post(self.api_url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                # 根据DeepSeek API的响应格式提取文本
                generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return generated_text
            else:
                logger.error(f"DeepSeek API调用失败: {response.status_code}, {response.text}")
                return f"API调用失败: {response.status_code}"

        except Exception as e:
            logger.error(f"文本生成失败: {str(e)}")
            raise e

    # 添加generate_text方法作为generate的别名，保持API兼容性
    def generate_text(self, input_text, max_length=4096):
        """生成文本（别名方法）"""
        return self.generate(input_text, max_length)


# 创建模型单例
text_generation_model = TextGenerationModel()
