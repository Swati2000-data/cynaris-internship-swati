
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "retail.db"

def setup_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        city TEXT,
        signup_date TEXT
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        unit_price REAL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)

    customers = [
        (1, "Aarav", "Bengaluru", "2025-01-10"),
        (2, "Diya", "Mumbai", "2025-02-15"),
        (3, "Rohan", "Delhi", "2025-03-20"),
        (4, "Ananya", "Bengaluru", "2025-04-12"),
        (5, "Ishaan", "Pune", "2025-05-18")
    ]

    products = [
        (1, "Laptop", "Electronics", 55000),
        (2, "Headphones", "Electronics", 2500),
        (3, "Office Chair", "Furniture", 7500),
        (4, "Notebook", "Stationery", 100),
        (5, "Desk", "Furniture", 12000)
    ]

    orders = [
        (101, 1, "2025-06-01", "Completed"),
        (102, 2, "2025-06-03", "Pending"),
        (103, 3, "2025-06-05", "Completed"),
        (104, 4, "2025-06-07", "Completed"),
        (105, 5, "2025-06-10", "Cancelled"),
        (106, 1, "2025-07-02", "Completed"),
        (107, 2, "2025-07-05", "Completed"),
        (108, 4, "2025-07-08", "Pending")
    ]

    order_items = [
        (1, 101, 1, 1, 55000),
        (2, 101, 2, 2, 2500),
        (3, 102, 3, 1, 7500),
        (4, 103, 4, 5, 100),
        (5, 103, 5, 1, 12000),
        (6, 104, 2, 1, 2500),
        (7, 105, 3, 2, 7500),
        (8, 106, 1, 1, 55000),
        (9, 107, 5, 1, 12000),
        (10, 108, 4, 10, 100)
    ]

    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    cursor.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", order_items)

    connection.commit()

    for table in ["customers", "products", "orders", "order_items"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]} records")

    connection.close()
    print(f"\nDatabase created successfully: {DB_PATH}")

if __name__ == "__main__":
    setup_database()
