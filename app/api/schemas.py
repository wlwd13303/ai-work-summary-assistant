from pydantic import BaseModel, Field


class TextGenerationRequest(BaseModel):
    content: str = Field(..., description="工作内容要点文本")


class TextGenerationResponse(BaseModel):
    generated_text: str = Field(..., description="生成的周报文本")


class ErrorResponse(BaseModel):
    detail: str
