
import polars as pl
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
# 2. LOAD DATASET
# ==========================================

print("\n========== POLARS ANALYSIS ==========")

if not CSV_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {CSV_FILE}"
    )

start = time.perf_counter()

df = pl.read_csv(
    CSV_FILE,
    try_parse_dates=True
)

polars_load_time = time.perf_counter() - start

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ==========================================
# 3. ANALYTICAL OPERATIONS
# ==========================================

start = time.perf_counter()


# Q1: Total Records
q1 = df.height


# Q2: Revenue Summary
q2 = df.select(
    pl.col("Revenue").sum().alias("total_revenue"),
    pl.col("Revenue").mean().alias("average_revenue")
)


# Q3: Revenue by Country
q3 = (
    df.group_by("Country")
    .agg(
        pl.col("Revenue").sum().alias("total_revenue")
    )
    .sort("total_revenue", descending=True)
    .head(10)
)


# Q4: Top 10 Products
q4 = (
    df.group_by("StockCode")
    .agg(
        pl.col("Revenue").sum().alias("total_revenue")
    )
    .sort("total_revenue", descending=True)
    .head(10)
)


# Q5: Monthly Revenue
q5 = (
    df.group_by(
        pl.col("InvoiceDate")
        .dt.strftime("%Y-%m")
        .alias("month")
    )
    .agg(
        pl.col("Revenue").sum().alias("monthly_revenue")
    )
    .sort("month")
)


polars_analysis_time = time.perf_counter() - start


# ==========================================
# 4. DISPLAY RESULTS
# ==========================================

print("\nQ1 - Total Records")
print(q1)

print("\nQ2 - Revenue Summary")
print(q2)

print("\nQ3 - Revenue by Country")
print(q3)

print("\nQ4 - Top 10 Products")
print(q4)

print("\nQ5 - Monthly Revenue")
print(q5)


# ==========================================
# 5. PERFORMANCE
# ==========================================

print("\n========== POLARS PERFORMANCE ==========")

print(f"Load Time: {polars_load_time:.6f} seconds")

print(
    f"Analysis Time: {polars_analysis_time:.6f} seconds"
)

print(
    f"Total Time: "
    f"{polars_load_time + polars_analysis_time:.6f} seconds"
)

print("\nPolars analysis completed successfully!")
