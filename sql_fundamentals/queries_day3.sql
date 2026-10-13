
-- Week 1 - Day 3: SQL Aggregations
-- Database: MySQL
-- Table: sales
use sales_db;

-- Query 1: Count the total number of sales records
SELECT COUNT(*) AS total_sales
FROM sales;

Describe sales;
ALTER TABLE sales
ADD COLUMN revenue DECIMAL(12,2);

UPDATE sales
SET revenue = quantity * unit_price
WHERE sale_id > 0;

SELECT sale_id, quantity, unit_price, revenue
FROM sales
LIMIT 10;

-- Query 2: Calculate total revenue
SELECT SUM(revenue) AS total_revenue
FROM sales;

-- Query 3: Calculate average revenue per sales record
SELECT AVG(revenue) AS average_revenue
FROM sales;

-- Query 4: Find the highest and lowest sale revenue
SELECT
    MAX(revenue) AS highest_sale,
    MIN(revenue) AS lowest_sale
FROM sales;

-- Query 5: Summarize revenue by region
-- HAVING filters regions with revenue above 10000
ALTER TABLE sales
ADD COLUMN region VARCHAR(50);

UPDATE sales
SET region = CASE
    WHEN MOD(sale_id, 3) = 0 THEN 'North'
    WHEN MOD(sale_id, 3) = 1 THEN 'South'
    ELSE 'West'
END
WHERE sale_id > 0;

SELECT region, COUNT(*) AS number_of_sales
FROM sales
GROUP BY region;

SELECT
    region,
    COUNT(*) AS number_of_sales,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
HAVING SUM(revenue) > 10000;

-- Query 6: Summarize sales by product category
-- Show only categories with at least 10 sales records
SELECT
    category,
    COUNT(*) AS number_of_sales,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS average_revenue
FROM sales
GROUP BY category
HAVING COUNT(*) >= 10;

-- Query 7: Summarize revenue by month
SELECT
    DATE_FORMAT(sale_date, '%Y-%m') AS sales_month,
    COUNT(*) AS number_of_sales,
    SUM(revenue) AS monthly_revenue
FROM sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY sales_month;

-- Query 8: Summarize revenue by region and category
-- Show only region-category combinations with revenue above 5000
SELECT
    region,
    category,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS average_revenue
FROM sales
GROUP BY region, category
HAVING SUM(revenue) > 5000
ORDER BY total_revenue DESC;

-- Query 9: Calculate a running total of revenue
-- Window function: SUM() OVER()
SELECT
    sale_id,
    sale_date,
    region,
    revenue,
    SUM(revenue) OVER (
        ORDER BY sale_date, sale_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM sales
ORDER BY sale_date, sale_id;
