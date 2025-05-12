from transformers import AutoTokenizer, AutoModel
import torch
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class TextGenerationModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.initialized = False

    def initialize(self):
        '''初始化模型和分词器'''
        try:
            logger.info(f"Loading model from {settings.MODEL_PATH}...")
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME, trust_remote_code=True)
            self.model = AutoModel.from_pretrained(settings.MODEL_NAME, trust_remote_code=True)
            # 如果有GPU，将模型移至GPU
            if settings.DEVICE == 'cpu' and torch.cuda.is_available():
                self.model = self.model.to(settings.DEVICE)
            self.initialized = True
            logger.info("Model initialized successfully.")
        except Exception as e:
            logger.error("Model initialized successfully.")

    def generate(self, input_text, max_length=1024):
        '''生成文本'''
        if not self.initialized:
            self.initialize()
        try:
            #  为周报生成构建提示词
            prompt = f"""请根据以下工作内容，生成一份结构良好、表达专业的工作周报：
                    {input_text}
                    请生成包含以下部分的周报：
                    1. 本周工作内容和成果
                    2. 下周工作计划
                    3. 工作中遇到的问题和解决方案（如果有）
                    4. 工作心得（如果有）
                    """
            if hasattr(self.model, 'chat') and callable(self.model.chat):
                # ChatGLM等模型
                response, _ = self.model.chat(self.tokenizer, prompt=prompt, history=[])
            else:
                # 一般的生成式模型
                inputs = self.tokenizer(prompt, return_tensors='pt')
                if settings.DEVICE == 'cpu' and torch.cuda.is_available():
                    inputs = {k: v.to(settings.DEVICE) for k, v in inputs.items()}
                outputs = self.model.generate(**inputs, max_length=max_length, num_return_sequences=1)
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response

        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")

# 创建模型单例
text_generation_model = TextGenerationModel()