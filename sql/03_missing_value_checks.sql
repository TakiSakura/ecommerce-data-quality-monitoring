-- Missing Value Checks


-- 1. Orders with delivered status but missing delivered date
SELECT
    order_id,
    order_status,
    order_delivered_customer_date
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NULL;


-- 2. Orders missing approved timestamp
SELECT
    order_id,
    order_approved_at
FROM orders
WHERE order_approved_at IS NULL;


-- 3. Products missing category name
SELECT
    product_id
FROM products
WHERE product_category_name IS NULL;


-- 4. Products missing dimensions
SELECT
    product_id
FROM products
WHERE product_weight_g IS NULL
   OR product_length_cm IS NULL
   OR product_height_cm IS NULL
   OR product_width_cm IS NULL;


-- 5. Payments missing payment value
SELECT
    order_id
FROM payments
WHERE payment_value IS NULL;


-- 6. Reviews missing review score
SELECT
    review_id
FROM reviews
WHERE review_score IS NULL;