
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from Analysis.sql_analyst.Engine import get_vanna

vn = get_vanna()

# Train Vanna with database schema
schema = vn.run_sql("""
    SELECT sql
    FROM sqlite_master
    WHERE type = 'table'
      AND name NOT LIKE 'sqlite_%'
""")

for ddl in schema["sql"].dropna():
    vn.train(ddl=ddl)

# Five example question-and-SQL pairs
training_data = [
    (
        "Show the top 5 customers by total spending.",
        """
        SELECT c.customer_name,
               SUM(oi.quantity * oi.unit_price) AS total_spending
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spending DESC
        LIMIT 5
        """
    ),
    (
        "Show total revenue by product category.",
        """
        SELECT p.category,
               SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'Completed'
        GROUP BY p.category
        ORDER BY total_revenue DESC
        """
    ),
    (
        "How many orders are pending?",
        """
        SELECT COUNT(*) AS pending_orders
        FROM orders
        WHERE status = 'Pending'
        """
    ),
    (
        "Show the top 3 products by units sold.",
        """
        SELECT p.product_name,
               SUM(oi.quantity) AS units_sold
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'Completed'
        GROUP BY p.product_id, p.product_name
        ORDER BY units_sold DESC
        LIMIT 3
        """
    ),
    (
        "Show monthly revenue.",
        """
        SELECT strftime('%Y-%m', o.order_date) AS month,
               SUM(oi.quantity * oi.unit_price) AS monthly_revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY month
        ORDER BY month
        """
    )
]

for question, sql in training_data:
    vn.train(question=question, sql=sql)
    print(f"Trained: {question}")

print("\nVanna training completed successfully.")
