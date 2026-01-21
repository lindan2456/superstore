from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mcp_server.db import get_connection
from mcp_server.sql_validator import validate_sql

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str

@app.post("/query")
def run_query(req: QueryRequest):
    try:
        validate_sql(req.sql)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(req.sql)
        rows = cur.fetchall()
        columns = [c[0] for c in cur.description]
        return {
            "columns": columns,
            "rows": rows
        }
    finally:
        cur.close()
        conn.close()
