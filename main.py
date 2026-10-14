import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# STEP 0
print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))

# STEP 1
df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees
JOIN offices
    USING(officeCode)
WHERE city = 'Boston'
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
SELECT offices.officeCode, offices.city
FROM offices
LEFT JOIN employees
    ON offices.officeCode = employees.officeCode
WHERE employees.employeeNumber IS NULL
""", conn)

# STEP 3
df_employee = pd.read_sql("""
SELECT firstName, lastName, city, state
FROM employees
LEFT JOIN offices
    USING(officeCode)
ORDER BY firstName, lastName
""", conn)

# STEP 4
df_contacts = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
    USING(customerNumber)
WHERE orderNumber IS NULL
ORDER BY contactLastName
""", conn)

# STEP 5
df_payment = pd.read_sql("""
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments
    USING(customerNumber)
ORDER BY CAST(amount AS REAL) DESC
""", conn)

# STEP 6
df_credit = pd.read_sql("""
SELECT employeeNumber, firstName, lastName,
       COUNT(customerNumber) AS n_customers
FROM employees
JOIN customers
    ON employeeNumber = salesRepEmployeeNumber
GROUP BY employeeNumber
HAVING AVG(creditLimit) > 90000
ORDER BY n_customers DESC
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
SELECT productName,
       COUNT(orderNumber) AS numorders,
       SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderdetails
    USING(productCode)
GROUP BY productCode
ORDER BY totalunits DESC
""", conn)

# STEP 8
df_total_customers = pd.read_sql("""
SELECT productName, productCode,
       COUNT(DISTINCT customerNumber) AS numpurchasers
FROM products
JOIN orderdetails
    USING(productCode)
JOIN orders
    USING(orderNumber)
GROUP BY productCode
ORDER BY numpurchasers DESC
""", conn)

# STEP 9
df_customers = pd.read_sql("""
SELECT COUNT(customerNumber) AS n_customers,
       offices.officeCode, offices.city
FROM customers
JOIN employees
    ON customers.salesRepEmployeeNumber = employees.employeeNumber
JOIN offices
    ON employees.officeCode = offices.officeCode
GROUP BY offices.officeCode
""", conn)

# STEP 10
df_under_20 = pd.read_sql("""
SELECT DISTINCT employees.employeeNumber, employees.firstName,
       employees.lastName, offices.city, offices.officeCode
FROM employees
JOIN offices
    ON employees.officeCode = offices.officeCode
JOIN customers
    ON customers.salesRepEmployeeNumber = employees.employeeNumber
JOIN orders
    ON orders.customerNumber = customers.customerNumber
JOIN orderdetails
    ON orderdetails.orderNumber = orders.orderNumber
WHERE orderdetails.productCode IN (
    SELECT productCode
    FROM orderdetails
    JOIN orders
        USING(orderNumber)
    GROUP BY productCode
    HAVING COUNT(DISTINCT customerNumber) < 20
)
ORDER BY employees.lastName, employees.firstName
""", conn)

# Print results
print("\nSTEP 1: Boston employees")
print(df_boston)

print("\nSTEP 2: Offices with zero employees")
print(df_zero_emp)

print("\nSTEP 3: All employees with office city/state")
print(df_employee)

print("\nSTEP 4: Customers with no orders")
print(df_contacts)
print("Row count:", len(df_contacts))

print("\nSTEP 5: Payments")
print(df_payment.head(10))

print("\nSTEP 6: High credit limit reps")
print(df_credit)
print("Row count:", len(df_credit))

print("\nSTEP 7: Top-selling products")
print(df_product_sold.head(10))

print("\nSTEP 8: Purchasers per product")
print(df_total_customers.head(10))

print("\nSTEP 9: Customers per office")
print(df_customers)

print("\nSTEP 10: Employees who sold products ordered by fewer than 20 customers")
print(df_under_20)

conn.close()