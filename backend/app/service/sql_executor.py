from typing import Any

from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.schema import QueryResult
from app.service.sql_validator import validate_and_rewrite_sql

async def execute_readonly_sql(session: AsyncSession, sql: str) -> QueryResult:
    """Validate and execute SQL in a read-only transaction with a timeout."""
    validated_sql = validate_and_rewrite_sql(sql)

    await session.exec(text("SET TRANSACTION READ ONLY"))
    result = await session.exec(text(validated_sql))
    rows: list[dict[str, Any]] = [dict(row) for row in result.mappings().all()]

    return QueryResult(
        sql=validated_sql,
        columns=list(result.keys()),
        rows=rows,
    )

