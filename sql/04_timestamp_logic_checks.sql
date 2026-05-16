-- Timestamp Logic Checks
-- These checks identify inconsistent order lifecycle timestamps.


-- 1. Orders where approved time is earlier than purchase time
SELECT
    order_id,
    order_purchase_timestamp,
    order_approved_at
FROM orders
WHERE order_approved_at IS NOT NULL
  AND datetime(order_approved_at) < datetime(order_purchase_timestamp);


-- 2. Orders where carrier delivery date is earlier than approved time
SELECT
    order_id,
    order_approved_at,
    order_delivered_carrier_date
FROM orders
WHERE order_approved_at IS NOT NULL
  AND order_delivered_carrier_date IS NOT NULL
  AND datetime(order_delivered_carrier_date) < datetime(order_approved_at);


-- 3. Orders where customer delivery date is earlier than carrier delivery date
SELECT
    order_id,
    order_delivered_carrier_date,
    order_delivered_customer_date
FROM orders
WHERE order_delivered_carrier_date IS NOT NULL
  AND order_delivered_customer_date IS NOT NULL
  AND datetime(order_delivered_customer_date) < datetime(order_delivered_carrier_date);


-- 4. Delivered orders missing customer delivery date
SELECT
    order_id,
    order_status,
    order_delivered_customer_date
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NULL;


-- 5. Delivered orders missing approved timestamp
SELECT
    order_id,
    order_status,
    order_approved_at
FROM orders
WHERE order_status = 'delivered'
  AND order_approved_at IS NULL;


-- 6. Orders delivered later than estimated delivery date
-- This is not necessarily a data error. It is an operational KPI.
SELECT
    order_id,
    order_delivered_customer_date,
    order_estimated_delivery_date
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND date(order_delivered_customer_date) > date(order_estimated_delivery_date);