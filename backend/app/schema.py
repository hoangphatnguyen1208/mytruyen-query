from typing import Any

from pydantic import BaseModel, Field

class GeneratedQuery(BaseModel):
    sql: str = Field(..., description="The generated SQL query.")
    
class NaturalLanguageQueryRequest(BaseModel):
    question: str = Field(..., description="The natural language question to be converted into SQL.")

class QueryResult(BaseModel):
    sql: str = Field(..., description="The validated SQL that was executed.")
    columns: list[str] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)
