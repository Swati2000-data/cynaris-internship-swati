
| Criteria        | Pandas                  | DuckDB                         | Polars 

| Primary purpose | Data analysis           | SQL analytics                  | DataFrame analytics           |
| Query language  | Python                  | SQL                            | Python expressions            |
| Performance     | Good                    | Excellent for analytical SQL   | High-performance processing   |
| Memory usage    | Can be memory-intensive | Efficient analytical execution | Efficient columnar processing |
| Best use case   | Data cleaning and EDA   | Large CSV/Parquet SQL queries  | Fast data transformation      |





## Benchmark Results

Dataset: Online Retail
Records: 100,000

| Library | Load Time | Analysis Time | Total Time |
|---|---|---|---|
| Pandas | See benchmark_results.csv | See benchmark_results.csv | See benchmark_results.csv |
| DuckDB | See benchmark_results.csv | See benchmark_results.csv | See benchmark_results.csv |
| Polars | See benchmark_results.csv | See benchmark_results.csv | See benchmark_results.csv |

## Observations

- Pandas provides familiar and convenient DataFrame operations.
- DuckDB makes analytical SQL queries easy to execute directly on CSV data.
- Polars provides expressive DataFrame operations with high-performance execution.
- Actual performance depends on hardware, dataset size and workload.



