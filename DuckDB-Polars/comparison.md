# Pandas vs DuckDB vs Polars

| Criteria | Pandas | DuckDB | Polars |
|---|---|---|---|
| Primary purpose | Data manipulation and analysis | SQL-based analytical queries | High-performance DataFrame processing |
| Syntax | Python DataFrame operations | SQL queries | Python DataFrame expressions |
| Execution model | Eager | SQL query execution | Eager and lazy |
| Performance | Slower in this benchmark | Efficient SQL analytics | Fastest in this benchmark |
| Best use case | General data analysis and cleaning | Analytical SQL on CSV and Parquet files | Fast data transformations and large-scale DataFrame operations |

## Benchmark Observations

Dataset: 100,000 rows

| Library | Load Time (s) | Analysis Time (s) | Total Time (s) |
|---|---:|---:|---:|
| Pandas | 0.371389 | 0.780350 | 1.151739 |
| DuckDB | 0.218369 | 0.108610 | 0.326980 |
| Polars | 0.069615 | 0.032761 | 0.102376 |

## Key Findings
- Pandas provides familiar and flexible DataFrame operations.
- DuckDB makes analytical SQL queries convenient without requiring a separate database server.
- Polars provides eager and lazy DataFrame processing with strong performance.
- Polars achieved the lowest execution time in this particular benchmark.

## Conclusion
Each library has different strengths. Pandas is useful for general-purpose data analysis, DuckDB is effective for SQL-based analytics, and Polars is suitable for performance-focused DataFrame processing.

**Note:** These timings are from a single run. Loading methods differ slightly: DuckDB creates a table from the CSV, while Pandas and Polars load the CSV into DataFrames. Results may vary across machines and repeated runs.