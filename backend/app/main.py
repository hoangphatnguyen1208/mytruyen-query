from fastapi import FastAPI

from app.api.v1.nl_query import router as nl_query_router
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(nl_query_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}

