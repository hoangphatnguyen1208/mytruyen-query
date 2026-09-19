from sqlglot import exp, parse
from sqlglot.errors import ParseError
from sqlglot.optimizer.qualify import qualify

from app.service.catalog import TABLES


class InvalidSQL(ValueError):
    """Raised when generated SQL is unsafe or outside the catalog."""


BLOCKED_NODES = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Merge,
    exp.Create,
    exp.Drop,
    exp.Alter,
    exp.Command,
    exp.Transaction,
)


def _catalog_schema() -> dict[str, dict[str, str]]:
    return {
        table_name: {
            column_name: metadata["type"]
            for column_name, metadata in table["columns"].items()
        }
        for table_name, table in TABLES.items()
    }


def _literal_limit(expression: exp.Query) -> int | None:
    limit = expression.args.get("limit")
    if limit is None:
        return None
    value = limit.expression
    if isinstance(value, exp.Literal) and not value.is_string:
        return int(value.this)
    raise InvalidSQL("LIMIT must be a positive integer literal")


def validate_and_rewrite_sql(sql: str, max_limit: int = 100) -> str:
    """Validate one read-only PostgreSQL query and enforce a row limit."""
    try:
        statements = parse(sql.strip(), read="postgres")
    except ParseError as error:
        raise InvalidSQL(f"Invalid PostgreSQL SQL: {error}") from error

    if len(statements) != 1:
        raise InvalidSQL("Exactly one SQL statement is required")

    expression = statements[0]
    if not isinstance(expression, exp.Query):
        raise InvalidSQL("Only SELECT queries are allowed")
    if any(expression.find(node_type) is not None for node_type in BLOCKED_NODES):
        raise InvalidSQL("The query contains a forbidden operation")

    cte_names = {cte.alias_or_name for cte in expression.find_all(exp.CTE)}
    for table in expression.find_all(exp.Table):
        table_name = table.name
        if table_name not in cte_names and table_name not in TABLES:
            raise InvalidSQL(f"Table is not allowed: {table_name}")
        if table.catalog or table.db:
            raise InvalidSQL("Catalog-qualified and schema-qualified tables are not allowed")

    try:
        expression = qualify(
            expression,
            dialect="postgres",
            schema=_catalog_schema(),
            validate_qualify_columns=True,
            quote_identifiers=False,
        )
    except Exception as error:
        raise InvalidSQL(f"A table or column is invalid: {error}") from error

    current_limit = _literal_limit(expression)
    if current_limit is None or current_limit > max_limit:
        expression = expression.limit(max_limit, copy=False)
    elif current_limit < 1:
        raise InvalidSQL("LIMIT must be greater than zero")

    return expression.sql(dialect="postgres", pretty=True)

