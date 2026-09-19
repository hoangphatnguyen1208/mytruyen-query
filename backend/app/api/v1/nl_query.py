from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.depend import SessionDep
from app.schema import GeneratedQuery, NaturalLanguageQueryRequest, QueryResult
from app.service.sql_generator import generate_sql
from app.service.sql_executor import execute_readonly_sql
from app.service.sql_validator import InvalidSQL


router = APIRouter(prefix="/nl-query", tags=["Natural Language Query"])


@router.post("/preview", response_model=GeneratedQuery)
async def preview_query(payload: NaturalLanguageQueryRequest) -> GeneratedQuery:
    """Generate SQL and return it only after structural validation."""
    try:
        return await generate_sql(payload.question)
    except InvalidSQL as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    
@router.post("/query", response_model=QueryResult)
async def execute_query(
    session: SessionDep,
    payload: NaturalLanguageQueryRequest,
) -> QueryResult:
    """Generate SQL, validate it, and execute it against the database."""
    try:
        generated_query = await generate_sql(payload.question)
        return await execute_readonly_sql(
            session=session,
            sql=generated_query.sql,
        )
    except InvalidSQL as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Database execution error.") from error

