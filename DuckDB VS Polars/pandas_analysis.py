
import pandas as pd
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent

CSV_FILE = (
    BASE_DIR / "data" / "processed" /
    "online_retail_100k.csv"
)

print("\n========== PANDAS ANALYSIS ==========")

# Load dataset
start = time.perf_counter()

df = pd.read_csv(
    CSV_FILE,
    parse_dates=["InvoiceDate"]
)

pandas_load_time = time.perf_counter() - start

# Five analytical operations
start = time.perf_counter()

q1 = len(df)

q2 = df["Revenue"].agg(["sum", "mean"])

q3 = (
    df.groupby("Country")["Revenue"]
    .sum()
    .nlargest(10)
)

q4 = (
    df.groupby("StockCode")["Revenue"]
    .sum()
    .nlargest(10)
)

q5 = (
    df.groupby(df["InvoiceDate"].dt.strftime("%Y-%m"))
    ["Revenue"].sum().sort_index()
)

pandas_analysis_time = time.perf_counter() - start

print("\nQ1 - Total Records:", q1)
print("\nQ2 - Revenue Summary:\n", q2)
print("\nQ3 - Revenue by Country:\n", q3)
print("\nQ4 - Top 10 Products:\n", q4)
print("\nQ5 - Monthly Revenue:\n", q5)

print("\n========== PANDAS PERFORMANCE ==========")

print(f"Load Time: {pandas_load_time:.6f} seconds")
print(f"Analysis Time: {pandas_analysis_time:.6f} seconds")
print(
    f"Total Time: "
    f"{pandas_load_time + pandas_analysis_time:.6f} seconds"
)
