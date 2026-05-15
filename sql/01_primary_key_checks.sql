-- Primary Key Uniqueness Checks
-- These checks identify duplicate IDs in key business tables.


-- 1. Check duplicate customer_id in customers
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- 2. Check duplicate order_id in orders
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- 3. Check duplicate product_id in products
SELECT
    product_id,
    COUNT(*) AS duplicate_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;


-- 4. Check duplicate seller_id in sellers
SELECT
    seller_id,
    COUNT(*) AS duplicate_count
FROM sellers
GROUP BY seller_id
HAVING COUNT(*) > 1;


-- 5. Check duplicate category name in category_translation
SELECT
    product_category_name,
    COUNT(*) AS duplicate_count
FROM category_translation
GROUP BY product_category_name
HAVING COUNT(*) > 1;