-- Payment Reconciliation Checks


-- 1. Compare total payment value with total item price + freight by order
WITH payment_totals AS (
    SELECT
        order_id,
        ROUND(SUM(payment_value), 2) AS total_payment_value
    FROM payments
    GROUP BY order_id
),

item_totals AS (
    SELECT
        order_id,
        ROUND(SUM(price + freight_value), 2) AS total_item_value
    FROM order_items
    GROUP BY order_id
)

SELECT
    p.order_id,
    p.total_payment_value,
    i.total_item_value,
    ROUND(p.total_payment_value - i.total_item_value, 2) AS difference
FROM payment_totals p
JOIN item_totals i
    ON p.order_id = i.order_id
WHERE ABS(ROUND(p.total_payment_value - i.total_item_value, 2)) > 0.01
ORDER BY ABS(difference) DESC;