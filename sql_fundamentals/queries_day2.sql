
create database EMP;
use EMP;

-- Create Departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

-- Create Employees table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(50),
    department_id INT,
    manager_id INT,
    salary DECIMAL(10, 2)
);

-- Insert sample departments
INSERT INTO departments VALUES
(1, 'IT'),
(2, 'HR'),
(3, 'Finance'),
(4, 'Marketing');

-- Insert sample employees
INSERT INTO employees VALUES
(101, 'Asha', 1, NULL, 60000),
(102, 'Rahul', 2, 101, 45000),
(103, 'Priya', 1, 101, 55000),
(104, 'Kiran', NULL, 102, 40000);

-- INNER JOIN

SELECT e.employee_name, d.department_name
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id;
    
-- Left Join
SELECT e.employee_name, d.department_name
FROM employees e
LEFT JOIN departments d
    ON e.department_id = d.department_id;
    
-- Right Join
SELECT e.employee_name, d.department_name
FROM employees e
RIGHT JOIN departments d
    ON e.department_id = d.department_id;
    
-- full Join
SELECT
    e.employee_name,
    d.department_name
FROM employees e
LEFT JOIN departments d
    ON e.department_id = d.department_id

UNION

SELECT
    e.employee_name,
    d.department_name
FROM employees e
RIGHT JOIN departments d
    ON e.department_id = d.department_id;
    
-- Self Join
SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e
LEFT JOIN employees m
    ON e.manager_id = m.employee_id;
    
    -- Explain and fix duplicate rows
-- JOINs can return duplicate-looking rows when a record matches multiple records in the other table.
-- For example, one department can have multiple employees. Each employee will appear as a separate row in the joined output. This is expected behavior, not necessarily an error.
    SELECT DISTINCT
    d.department_name
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id;