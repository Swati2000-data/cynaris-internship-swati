
import duckdb
import time
from pathlib import Path


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).parent

CSV_FILE = (
    BASE_DIR / "data" / "processed" /
    "online_retail_100k.csv"
)


# ==========================================
# 2. DUCKDB CONNECTION
# ==========================================

print("\n========== DUCKDB ANALYSIS ==========")

if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {CSV_FILE}"
    )

con = duckdb.connect()


# ==========================================
# 3. LOAD DATASET
# ==========================================

start = time.perf_counter()

csv_path = CSV_FILE.as_posix().replace("'", "''")

con.execute(f"""
    CREATE TABLE retail AS
    SELECT *
    FROM read_csv_auto('{csv_path}')
""")

duckdb_load_time = time.perf_counter() - start

print("Dataset loaded successfully!")
print("Total records:", con.execute(
    "SELECT COUNT(*) FROM retail"
).fetchone()[0])


# ==========================================
# 4. ANALYTICAL SQL QUERIES
# ==========================================

queries = {

    # Q1: Total Records
    "Q1 - Total Records": """
        SELECT COUNT(*) AS total_records
        FROM retail
    """,

    # Q2: Revenue Summary
    "Q2 - Revenue Summary": """
        SELECT
            SUM(Revenue) AS total_revenue,
            AVG(Revenue) AS average_revenue
        FROM retail
    """,

    # Q3: Revenue by Country
    "Q3 - Revenue by Country": """
        SELECT
            Country,
            SUM(Revenue) AS total_revenue
        FROM retail
        GROUP BY Country
        ORDER BY total_revenue DESC
        LIMIT 10
    """,

    # Q4: Top 10 Products
    "Q4 - Top 10 Products": """
        SELECT
            StockCode,
            SUM(Revenue) AS total_revenue
        FROM retail
        GROUP BY StockCode
        ORDER BY total_revenue DESC
        LIMIT 10
    """,

    # Q5: Monthly Revenue
    "Q5 - Monthly Revenue": """
        SELECT
            STRFTIME(
                CAST(InvoiceDate AS TIMESTAMP),
                '%Y-%m'
            ) AS month,
            SUM(Revenue) AS monthly_revenue
        FROM retail
        GROUP BY month
        ORDER BY month
    """
}


# ==========================================
# 5. EXECUTE QUERIES
# ==========================================

duckdb_results = {}

start = time.perf_counter()

for name, query in queries.items():

    result = con.execute(query).df()

    duckdb_results[name] = result

duckdb_analysis_time = time.perf_counter() - start


# ==========================================
# 6. DISPLAY RESULTS
# ==========================================

for name, result in duckdb_results.items():

    print(f"\n{name}")
    print(result.to_string(index=False))


# ==========================================
# 7. EXECUTION TIME
# ==========================================

print("\n========== DUCKDB PERFORMANCE ==========")

print(
    f"Load Time: {duckdb_load_time:.6f} seconds"
)

print(
    f"Analysis Time: {duckdb_analysis_time:.6f} seconds"
)


# ==========================================
# 8. CLOSE CONNECTION
# ==========================================

con.close()

print("\nDuckDB analysis completed successfully!")
