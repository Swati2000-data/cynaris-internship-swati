# Online Retail Dataset — EDA Report

## 1. Dataset Overview

- Original rows: 541,909
- Cleaned rows: 536,641
- Columns: 10
- Duplicate rows identified before cleaning: 5,268

## 2. Data Quality

See `data_quality_report.csv` for missing values, data types, and unique-value counts.

## 3. Summary Statistics

See `summary_statistics.csv` for numeric summary statistics.

## 4. Business Insights

### 1. Peak revenue month

**Finding:** 2011-11 recorded the highest monthly revenue (£1,503,866.78).

**Suggested action:** Review seasonal demand and plan stock and promotions ahead of peak periods.

### 2. Leading country

**Finding:** United Kingdom generated the highest revenue (£9,001,744.09), representing 84.59% of sales.

**Suggested action:** Protect the leading market while assessing opportunities to grow in other countries.

### 3. Top product

**Finding:** DOTCOM POSTAGE generated the highest product revenue (£206,248.77).

**Suggested action:** Monitor availability and evaluate whether this product merits additional promotion.

### 4. Customer concentration

**Finding:** Customer 14646.0 generated the highest identified customer revenue (£280,206.02). Consider retention strategies for high-value customers.

**Suggested action:** Use customer retention and repeat-purchase analysis to support valuable customers.

### 5. Returns and cancellations

**Finding:** 10,587 rows had negative quantities, with an absolute transaction value of £893,979.73.

**Suggested action:** Investigate return reasons and cancellation patterns before making operational changes.

## 5. Generated Visualizations

- correlation_heatmap.png
- monthly_returns.png
- monthly_revenue_trend.png
- monthly_revenue_vs_orders.png
- numeric_distributions.png
- order_quantity_distribution.png
- revenue_by_day.png
- top_10_countries_revenue.png
- top_10_customers.png
- top_10_products_revenue.png

## 6. Limitations

- Revenue is calculated as Quantity multiplied by UnitPrice; it is not profit.
- Negative quantities and cancellation invoices require careful interpretation.
- Missing customer identifiers limit customer-level analysis.
- Correlation does not establish causation.
