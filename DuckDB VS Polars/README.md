# DuckDB vs Pandas vs Polars – Performance Benchmark

## Project Overview
This project compares Pandas, DuckDB, and Polars for analytical operations on a 100,000-row Online Retail dataset.

## Objectives
- Load and analyse a 100K-row CSV dataset.
- Execute five analytical queries using all three libraries.
- Benchmark data loading and analysis execution times.
- Compare syntax, performance, and use cases.

## Dataset
- **Source:** [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)
- Original records: 541,909
- Processed records: 100,000
- Additional column: Revenue = Quantity × UnitPrice

## Analytical Queries
1. Count total records.
2. Calculate total and average revenue.
3. Identify top 10 countries by revenue.
4. Identify top 10 stock codes by revenue.
5. Calculate monthly revenue.

## Technologies Used
Python, Pandas, DuckDB, Polars, SQL

## Benchmark Results

| Library | Load Time (s) | Analysis Time (s) | Total Time (s) |
|---|---:|---:|---:|
| Pandas | 0.371389 | 0.780350 | 1.151739 |
| DuckDB | 0.218369 | 0.108610 | 0.326980 |
| Polars | 0.069615 | 0.032761 | 0.102376 |

**Observation:** Polars achieved the lowest total execution time in this benchmark run.

## Project Structure
- `benchmark.py` – Complete benchmark workflow
- `pandas_analysis.py` – Pandas implementation
- `duckdb_analysis.py` – DuckDB SQL implementation
- `polars_analysis.py` – Polars implementation
- `comparison.md` – Technology comparison
- `outputs/benchmark_results.csv` – Benchmark results

## How to Run

Install dependencies:

```bash
pip install -r Requirements.txt
```

Run the complete benchmark:

```bash
python benchmark.py
```

The original Excel dataset should be placed in `data/` before running the preparation workflow.

## Conclusion
The benchmark demonstrates that all three libraries can perform the same analytical operations, with different execution models and performance characteristics. Polars was the fastest in this particular test.