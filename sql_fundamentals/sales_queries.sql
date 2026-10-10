
USE sales_db;

-- 1. Display all sales
SELECT * FROM sales;

-- 2. Filter sales from Bengaluru
SELECT customer_name, product, city
FROM sales
WHERE city = 'Bengaluru';

-- 3. AND operator
SELECT customer_name, product, unit_price
FROM sales
WHERE category = 'Electronics'
  AND unit_price > 1000;

-- 4. OR operator
SELECT customer_name, city
FROM sales
WHERE city = 'Bengaluru'
   OR city = 'Mysuru';

-- 5. NOT operator
SELECT customer_name, product, category
FROM sales
WHERE NOT category = 'Stationery';

-- 6. LIKE operator
SELECT customer_name
FROM sales
WHERE customer_name LIKE 'A%';

-- 7. IN operator
SELECT customer_name, payment_method
FROM sales
WHERE payment_method IN ('UPI', 'Card');

-- 8. BETWEEN operator
SELECT product, unit_price
FROM sales
WHERE unit_price BETWEEN 1000 AND 10000;

-- 9. IS NULL operator
SELECT customer_name, product, discount
FROM sales
WHERE discount IS NULL;

-- 10. Calculate revenue and sort
SELECT customer_name, product,
       quantity * unit_price AS revenue
FROM sales
ORDER BY revenue DESC;
