import requests
from dotenv import load_dotenv

load_dotenv()

from llm.ollama_client import call_llm

MCP_URL = "http://127.0.0.1:8001/query"

with open("schema/schema_context.txt") as f:
    SCHEMA_CONTEXT = f.read()


def extract_sql(llm_output: str) -> str:
    """
    Robustly extract SQL starting from SELECT.
    Handles explanations from small models.
    """
    text = llm_output.strip()
    lower = text.lower()
    idx = lower.find("select")

    if idx == -1:
        raise RuntimeError(f"LLM did not generate SQL:\n{text}")

    sql = text[idx:].strip()
    return sql


def ask_db(question: str):
    prompt = f"""
{SCHEMA_CONTEXT}

User question:
{question}

SQL:
"""

    raw = call_llm(prompt)
    sql = extract_sql(raw)

    resp = requests.post(
        MCP_URL,
        json={"sql": sql},
        timeout=50
    )

    if resp.status_code != 200:
        raise RuntimeError(resp.text)

    data = resp.json()

    return {
        "question": question,
        "sql": sql,
        "columns": data["columns"],
        "rows": data["rows"]
    }
