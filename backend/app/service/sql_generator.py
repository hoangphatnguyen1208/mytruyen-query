import json

from google import genai
from google.genai import types

from fastapi import HTTPException
from app.core.config import settings
from app.schema import GeneratedQuery
from app.service.catalog import build_llm_catalog
from app.service.sql_validator import validate_and_rewrite_sql


SYSTEM_INSTRUCTION = """
You translate natural-language questions into read-only PostgreSQL queries.

Rules:
- Use only tables and columns in the supplied catalog.
- Return exactly one SELECT statement. A WITH clause is allowed only when it ends in SELECT.
- Never use INSERT, UPDATE, DELETE, MERGE, DROP, ALTER, TRUNCATE, COPY, CALL, or DDL.
- Never access hidden, sensitive, system, or information-schema data.
- Apply the catalog's visibility rules, including book.published = true and
  chapter.published = true whenever those tables are queried.
- Use explicit JOIN conditions based on the relationships in the catalog.
- Select only fields needed to answer the question.
- Use PostgreSQL syntax.
- Do not wrap SQL in Markdown fences.
- Return the GeneratedQuery object described by the response schema.
"""


def build_prompt(question: str) -> str:
    return json.dumps(
        {"question": question, "catalog": build_llm_catalog()},
        ensure_ascii=False,
        indent=2,
    )


async def generate_sql(question: str) -> GeneratedQuery:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=build_prompt(question),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=GeneratedQuery,
                temperature=0.0,
            ),
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Failed to generate SQL: {error.message}") from error

    generated = GeneratedQuery.model_validate(response.parsed)
    generated.sql = validate_and_rewrite_sql(generated.sql)
    return generated

