use sales_db;
DESCRIBE sales;


-- Week 1 - Day 4: SQL Subqueries and CTEs
-- Database: MySQL
-- Table: sales

-- Query 1: Non-correlated subquery
-- Find sales whose value is above the average sale value.

SELECT
    sale_id,
    quantity,
    unit_price,
    quantity * unit_price AS sale_value
FROM sales
WHERE quantity * unit_price > (
    SELECT AVG(quantity * unit_price)
    FROM sales
)
ORDER BY sale_value DESC;


-- Query 2: Correlated subquery
-- Find the highest-value sale in each region.
-- If multiple sales tie for the highest value, return all of them.

SELECT
    s.sale_id,
    s.region,
    s.quantity * s.unit_price AS sale_value
FROM sales AS s
WHERE s.quantity * s.unit_price = (
    SELECT MAX(s2.quantity * s2.unit_price)
    FROM sales AS s2
    WHERE s2.region = s.region
)
ORDER BY s.region;


-- Query 3: Rewrite a nested subquery using a CTE.
-- Find sales above the average sale value.

WITH average_sales AS (
    SELECT AVG(quantity * unit_price) AS avg_sale_value
    FROM sales
)
SELECT
    s.sale_id,
    s.quantity * s.unit_price AS sale_value
FROM sales AS s
CROSS JOIN average_sales AS a
WHERE s.quantity * s.unit_price > a.avg_sale_value
ORDER BY sale_value DESC;


-- Query 4: Chain two CTEs in a single query.
-- First calculate revenue by region.
-- Then calculate the average regional revenue.
-- Finally find regions above that average.

WITH regional_sales AS (
    SELECT
        region,
        SUM(quantity * unit_price) AS total_revenue
    FROM sales
    GROUP BY region
),
average_regional_sales AS (
    SELECT AVG(total_revenue) AS avg_regional_revenue
    FROM regional_sales
)
SELECT
    rs.region,
    rs.total_revenue
FROM regional_sales AS rs
CROSS JOIN average_regional_sales AS ars
WHERE rs.total_revenue > ars.avg_regional_revenue
ORDER BY rs.total_revenue DESC;
