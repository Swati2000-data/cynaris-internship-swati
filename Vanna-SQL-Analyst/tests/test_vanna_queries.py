
import sys
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from Analysis.sql_analyst.Engine import get_vanna

DB_PATH = PROJECT_ROOT / "database" / "retail.db"

questions = [
    "Show all customers from Bengaluru.",
    "How many customers are there?",
    "Show the top 5 customers by total spending.",
    "Show total revenue by product category.",
    "How many orders are pending?",
    "Show the top 3 products by units sold.",
    "Show monthly revenue.",
    "List all completed orders.",
    "What is the average price of products?",
    "Which city has the most customers?"
]

vn = get_vanna()

def execute_read_only(sql):
    sql = sql.strip().rstrip(";")

    # Basic restriction: only a single SELECT or WITH query is accepted.
    if not sql.lower().startswith(("select", "with")):
        raise ValueError("Only SELECT queries are allowed.")

    connection = sqlite3.connect(
        f"file:{DB_PATH.as_posix()}?mode=ro",
        uri=True
    )

    try:
        cursor = connection.execute(sql)
        return cursor.fetchmany(100)
    finally:
        connection.close()


for number, question in enumerate(questions, start=1):
    print(f"\nTest {number}: {question}")

    try:
        sql = vn.generate_sql(question=question)
        print("Generated SQL:")
        print(sql)

        result = execute_read_only(sql)
        print("Query executed successfully.")
        print("Result:", result)

    except Exception as error:
        print("Test failed:", error)
