

-- 1. Orders with customer_id not found in customers
SELECT
    o.order_id,
    o.customer_id
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- 2. Payments with order_id not found in orders
SELECT
    p.order_id
FROM payments p
LEFT JOIN orders o
    ON p.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 3. Order items with order_id not found in orders
SELECT
    oi.order_id,
    oi.order_item_id
FROM order_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 4. Order items with product_id not found in products
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- 5. Order items with seller_id not found in sellers
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.seller_id
FROM order_items oi
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;


-- 6. Reviews with order_id not found in orders
SELECT
    r.review_id,
    r.order_id
FROM reviews r
LEFT JOIN orders o
    ON r.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 7. Products with category not found in category_translation
SELECT
    p.product_id,
    p.product_category_name
FROM products p
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE p.product_category_name IS NOT NULL
  AND ct.product_category_name IS NULL;