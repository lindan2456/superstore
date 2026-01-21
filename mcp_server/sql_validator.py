FORBIDDEN = [
    "insert", "update", "delete",
    "drop", "alter", "truncate", "--", ";"
]

ALLOWED_TABLES = ["orders", "returns", "people"]

def validate_sql(sql: str):
    q = sql.lower().strip()
    sql = sql.strip()
    if sql.endswith(";"):
        sql = sql[:-1]
    return sql    


    if not q.startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    for word in FORBIDDEN:
        if word in q:
            raise ValueError(f"Forbidden keyword detected: {word}")

    if "*" in q:
        raise ValueError("SELECT * is not allowed")

    if not any(t in q for t in ALLOWED_TABLES):
        raise ValueError("Query must reference allowed tables")

    if "limit" not in q and not any(
        agg in q for agg in ["count(", "sum(", "avg(", "min(", "max("]
    ):
        raise ValueError("LIMIT required for non-aggregate queries")
