from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.schemas import TextGenerationRequest, TextGenerationResponse
from app.models.text_generation import text_generation_model
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generation_report", response_model=TextGenerationResponse)
async def generation_report(request: TextGenerationRequest):
    """生成周报API"""
    try:
        # 初始化模型
        if not text_generation_model.initialized:
            text_generation_model.initialize()
        # 生成文本
        generated_text = text_generation_model.generate_text(request.content)
        return TextGenerationResponse(generated_text=generated_text)
    except Exception as e:
        logger.error(f"Error in generation_report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
