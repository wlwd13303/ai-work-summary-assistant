import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import text_generation

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应设置为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(response: Request, call_next):
    start_time = time.time()
    response = await call_next(response)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 包含路由
app.include_router(
    text_generation.router,
    prefix=f"{settings.APP_PREFIX}/text-generation",
    tags=["text-generation"],
)


@app.get("/")
def read_root():
    return {"message": "欢迎使用智汇周报API服务"}


@app.get("/healthy")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
