
import pandas as pd
import duckdb
import polars as pl

from pathlib import Path
import time


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).parent

RAW_FILE = BASE_DIR / "data" / "Online Retail.xlsx"
CSV_FILE = BASE_DIR / "data" / "processed" / "online_retail_100k.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. DATASET PREPARATION
# ==========================================

print("\n========== DATASET PREPARATION ==========")

df = pd.read_excel(RAW_FILE)

print("Original shape:", df.shape)

df = df[
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0) &
    (~df["InvoiceNo"].astype(str).str.startswith("C"))
].copy()

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

df = df.sample(n=100000, random_state=42)

df.to_csv(CSV_FILE, index=False)

print("Processed shape:", df.shape)
print("Dataset saved:", CSV_FILE)
print("Total revenue:", round(df["Revenue"].sum(), 2))


# ==========================================
# 3. PANDAS ANALYSIS
# ==========================================

print("\n========== PANDAS ANALYSIS ==========")

start = time.perf_counter()

pandas_df = pd.read_csv(
    CSV_FILE,
    parse_dates=["InvoiceDate"]
)

pandas_load_time = time.perf_counter() - start

start = time.perf_counter()

# Q1: Total records
q1_pandas = len(pandas_df)

# Q2: Revenue summary
q2_pandas = pandas_df["Revenue"].agg(["sum", "mean"])

# Q3: Revenue by country
q3_pandas = (
    pandas_df.groupby("Country")["Revenue"]
    .sum()
    .nlargest(10)
)

# Q4: Top 10 products
q4_pandas = (
    pandas_df.groupby("StockCode")["Revenue"]
    .sum()
    .nlargest(10)
)

# Q5: Monthly revenue
q5_pandas = (
    pandas_df.groupby(
        pandas_df["InvoiceDate"].dt.strftime("%Y-%m")
    )["Revenue"]
    .sum()
    .sort_index()
)

pandas_analysis_time = time.perf_counter() - start

print("Q1:", q1_pandas)
print("\nQ2:\n", q2_pandas)
print("\nQ3:\n", q3_pandas)
print("\nQ4:\n", q4_pandas)
print("\nQ5:\n", q5_pandas)


# ==========================================
# 4. DUCKDB ANALYSIS
# ==========================================

print("\n========== DUCKDB ANALYSIS ==========")

con = duckdb.connect()

start = time.perf_counter()

csv_path = CSV_FILE.as_posix().replace("'", "''")

con.execute(f"""
    CREATE TABLE retail AS
    SELECT * FROM read_csv_auto('{csv_path}')
""")

duckdb_load_time = time.perf_counter() - start

queries = {
    "Q1": """
        SELECT COUNT(*) AS total_records
        FROM retail
    """,

    "Q2": """
        SELECT
            SUM(Revenue) AS total_revenue,
            AVG(Revenue) AS average_revenue
        FROM retail
    """,

    "Q3": """
        SELECT Country, SUM(Revenue) AS total_revenue
        FROM retail
        GROUP BY Country
        ORDER BY total_revenue DESC
        LIMIT 10
    """,

    "Q4": """
        SELECT
            StockCode,
            SUM(Revenue) AS total_revenue
        FROM retail
        GROUP BY StockCode
        ORDER BY total_revenue DESC
        LIMIT 10
    """,

    "Q5": """
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

start = time.perf_counter()

duckdb_results = {}

for name, query in queries.items():
    duckdb_results[name] = con.execute(query).df()
    print(f"\n{name}:\n", duckdb_results[name])

duckdb_analysis_time = time.perf_counter() - start

con.close()


# ==========================================
# 5. POLARS ANALYSIS
# ==========================================

print("\n========== POLARS ANALYSIS ==========")

start = time.perf_counter()

polars_df = pl.read_csv(
    CSV_FILE,
    try_parse_dates=True
)

polars_load_time = time.perf_counter() - start

start = time.perf_counter()

# Q1: Total records
q1_polars = polars_df.height

# Q2: Revenue summary
q2_polars = polars_df.select(
    pl.col("Revenue").sum().alias("total_revenue"),
    pl.col("Revenue").mean().alias("average_revenue")
)

# Q3: Revenue by country
q3_polars = (
    polars_df.group_by("Country")
    .agg(pl.col("Revenue").sum().alias("total_revenue"))
    .sort("total_revenue", descending=True)
    .head(10)
)

# Q4: Top 10 products
q4_polars = (
    polars_df.group_by("StockCode")
    .agg(pl.col("Revenue").sum().alias("total_revenue"))
    .sort("total_revenue", descending=True)
    .head(10)
)

# Q5: Monthly revenue
q5_polars = (
    polars_df.group_by(
        pl.col("InvoiceDate").dt.strftime("%Y-%m").alias("month")
    )
    .agg(pl.col("Revenue").sum().alias("monthly_revenue"))
    .sort("month")
)

polars_analysis_time = time.perf_counter() - start

print("Q1:", q1_polars)
print("\nQ2:\n", q2_polars)
print("\nQ3:\n", q3_polars)
print("\nQ4:\n", q4_polars)
print("\nQ5:\n", q5_polars)


# ==========================================
# 6. PERFORMANCE COMPARISON
# ==========================================

print("\n========== PERFORMANCE COMPARISON ==========")

results = pd.DataFrame({
    "Library": ["Pandas", "DuckDB", "Polars"],

    "Load Time (seconds)": [
        pandas_load_time,
        duckdb_load_time,
        polars_load_time
    ],

    "Analysis Time (seconds)": [
        pandas_analysis_time,
        duckdb_analysis_time,
        polars_analysis_time
    ]
})

results["Total Time (seconds)"] = (
    results["Load Time (seconds)"] +
    results["Analysis Time (seconds)"]
)

results.to_csv(
    OUTPUT_DIR / "benchmark_results.csv",
    index=False
)

print(results.to_string(index=False))

print("\nBenchmark results saved successfully!")
print("\n========== PROJECT COMPLETED ==========")
