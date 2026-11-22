
from pathlib import Path
import sqlite3

from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "database" / "retail.db"


class LocalVanna(ChromaDB_VectorStore, Ollama):

    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)


def get_vanna():

    vn = LocalVanna(
        config={
            "model": "qwen2.5:3b",
            "path": str(PROJECT_ROOT / "chroma_db")
        }
    )

    vn.connect_to_sqlite(str(DATABASE_PATH))

    # Train using actual database schema
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, sql
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)

    for table_name, ddl in cursor.fetchall():
        if ddl:
            vn.train(ddl=ddl)

    connection.close()

    # Six example question-SQL pairs
    training_examples = [
        (
            "How many customers are there?",
            "SELECT COUNT(*) AS total_customers FROM customers"
        ),
        (
            "How many orders are pending?",
            "SELECT COUNT(*) AS pending_orders FROM orders WHERE status = 'Pending'"
        ),
        (
            "How many completed orders are there?",
            "SELECT COUNT(*) AS completed_orders FROM orders WHERE status = 'Completed'"
        ),
        (
            "How many products are available?",
            "SELECT COUNT(*) AS total_products FROM products"
        ),
        (
            "Show all orders with their status",
            "SELECT order_id, status FROM orders"
        ),
        (
            "What is the average order value of completed orders?",
            """
            WITH order_totals AS (
                SELECT
                    o.order_id,
                    SUM(oi.quantity * oi.unit_price) AS order_total
                FROM orders o
                JOIN order_items oi
                    ON o.order_id = oi.order_id
                WHERE o.status = 'Completed'
                GROUP BY o.order_id
            )
            SELECT AVG(order_total) AS average_order_value
            FROM order_totals
            """
        )
    ]

    for question, sql in training_examples:
        vn.train(question=question, sql=sql)

    return vn
