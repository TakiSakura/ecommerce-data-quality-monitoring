DATA_QUALITY_CHECKS = [
    # =========================
    # Primary Key Checks
    # =========================
    {
        "check_category": "primary_key",
        "check_name": "duplicate_customer_id",
        "severity": "CRITICAL",
        "query": """
            SELECT
                customer_id,
                COUNT(*) AS duplicate_count
            FROM customers
            GROUP BY customer_id
            HAVING COUNT(*) > 1;
        """
    },
    {
        "check_category": "primary_key",
        "check_name": "duplicate_order_id",
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id,
                COUNT(*) AS duplicate_count
            FROM orders
            GROUP BY order_id
            HAVING COUNT(*) > 1;
        """
    },
    {
        "check_category": "primary_key",
        "check_name": "duplicate_product_id",
        "severity": "CRITICAL",
        "query": """
            SELECT
                product_id,
                COUNT(*) AS duplicate_count
            FROM products
            GROUP BY product_id
            HAVING COUNT(*) > 1;
        """
    },
    {
        "check_category": "primary_key",
        "check_name": "duplicate_seller_id",
        "severity": "CRITICAL",
        "query": """
            SELECT
                seller_id,
                COUNT(*) AS duplicate_count
            FROM sellers
            GROUP BY seller_id
            HAVING COUNT(*) > 1;
        """
    },
    {
        "check_category": "primary_key",
        "check_name": "duplicate_category_name",
        "severity": "CRITICAL",
        "query": """
            SELECT
                product_category_name,
                COUNT(*) AS duplicate_count
            FROM category_translation
            GROUP BY product_category_name
            HAVING COUNT(*) > 1;
        """
    },

    # =========================
    # Foreign Key Checks
    # =========================
    {
        "check_category": "foreign_key",
        "check_name": "orders_customer_id_not_in_customers",
        "severity": "CRITICAL",
        "query": """
            SELECT
                o.order_id,
                o.customer_id
            FROM orders o
            LEFT JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL;
        """
    },
    {
        "check_category": "foreign_key",
        "check_name": "payments_order_id_not_in_orders",
        "severity": "CRITICAL",
        "query": """
            SELECT
                p.order_id
            FROM payments p
            LEFT JOIN orders o
                ON p.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
    },
    {
        "check_category": "foreign_key",
        "check_name": "order_items_order_id_not_in_orders",
        "severity": "CRITICAL",
        "query": """
            SELECT
                oi.order_id,
                oi.order_item_id
            FROM order_items oi
            LEFT JOIN orders o
                ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
    },
    {
        "check_category": "foreign_key",
        "check_name": "order_items_product_id_not_in_products",
        "severity": "CRITICAL",
        "query": """
            SELECT
                oi.order_id,
                oi.order_item_id,
                oi.product_id
            FROM order_items oi
            LEFT JOIN products p
                ON oi.product_id = p.product_id
            WHERE p.product_id IS NULL;
        """
    },
    {
        "check_category": "foreign_key",
        "check_name": "order_items_seller_id_not_in_sellers",
        "severity": "CRITICAL",
        "query": """
            SELECT
                oi.order_id,
                oi.order_item_id,
                oi.seller_id
            FROM order_items oi
            LEFT JOIN sellers s
                ON oi.seller_id = s.seller_id
            WHERE s.seller_id IS NULL;
        """
    },
    {
        "check_category": "foreign_key",
        "check_name": "reviews_order_id_not_in_orders",
        "severity": "CRITICAL",
        "query": """
            SELECT
                r.review_id,
                r.order_id
            FROM reviews r
            LEFT JOIN orders o
                ON r.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
    },
    {
        "check_category": "foreign_key",
        "check_name": "products_category_not_in_translation",
        "severity": "WARNING",
        "query": """
            SELECT
                p.product_id,
                p.product_category_name
            FROM products p
            LEFT JOIN category_translation ct
                ON p.product_category_name = ct.product_category_name
            WHERE p.product_category_name IS NOT NULL
              AND ct.product_category_name IS NULL;
        """
    },

    # =========================
    # Missing Value Checks
    # =========================
    {
        "check_category": "missing_value",
        "check_name": "delivered_orders_missing_delivery_date",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_status,
                order_delivered_customer_date
            FROM orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NULL;
        """
    },
    {
        "check_category": "missing_value",
        "check_name": "orders_missing_approved_timestamp",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_approved_at
            FROM orders
            WHERE order_approved_at IS NULL;
        """
    },
    {
        "check_category": "missing_value",
        "check_name": "products_missing_category_name",
        "severity": "WARNING",
        "query": """
            SELECT
                product_id
            FROM products
            WHERE product_category_name IS NULL;
        """
    },
    {
        "check_category": "missing_value",
        "check_name": "products_missing_dimensions",
        "severity": "WARNING",
        "query": """
            SELECT
                product_id
            FROM products
            WHERE product_weight_g IS NULL
               OR product_length_cm IS NULL
               OR product_height_cm IS NULL
               OR product_width_cm IS NULL;
        """
    },
    {
        "check_category": "missing_value",
        "check_name": "payments_missing_payment_value",
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id
            FROM payments
            WHERE payment_value IS NULL;
        """
    },
    {
        "check_category": "missing_value",
        "check_name": "reviews_missing_review_score",
        "severity": "WARNING",
        "query": """
            SELECT
                review_id
            FROM reviews
            WHERE review_score IS NULL;
        """
    },

    # =========================
    # Timestamp Logic Checks
    # =========================
    {
        "check_category": "timestamp_logic",
        "check_name": "approved_before_purchase",
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id,
                order_purchase_timestamp,
                order_approved_at
            FROM orders
            WHERE order_approved_at IS NOT NULL
              AND datetime(order_approved_at) < datetime(order_purchase_timestamp);
        """
    },
    {
        "check_category": "timestamp_logic",
        "check_name": "carrier_date_before_approved",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_approved_at,
                order_delivered_carrier_date
            FROM orders
            WHERE order_approved_at IS NOT NULL
              AND order_delivered_carrier_date IS NOT NULL
              AND datetime(order_delivered_carrier_date) < datetime(order_approved_at);
        """
    },
    {
        "check_category": "timestamp_logic",
        "check_name": "customer_delivery_before_carrier_date",
        "severity": "CRITICAL",
        "query": """
            SELECT
                order_id,
                order_delivered_carrier_date,
                order_delivered_customer_date
            FROM orders
            WHERE order_delivered_carrier_date IS NOT NULL
              AND order_delivered_customer_date IS NOT NULL
              AND datetime(order_delivered_customer_date) < datetime(order_delivered_carrier_date);
        """
    },
    {
        "check_category": "timestamp_logic",
        "check_name": "delivered_orders_missing_customer_delivery_date",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_status,
                order_delivered_customer_date
            FROM orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NULL;
        """
    },
    {
        "check_category": "timestamp_logic",
        "check_name": "delivered_orders_missing_approved_timestamp",
        "severity": "WARNING",
        "query": """
            SELECT
                order_id,
                order_status,
                order_approved_at
            FROM orders
            WHERE order_status = 'delivered'
              AND order_approved_at IS NULL;
        """
    },
    {
        "check_category": "timestamp_logic",
        "check_name": "orders_delivered_later_than_estimated",
        "severity": "INFO",
        "query": """
            SELECT
                order_id,
                order_delivered_customer_date,
                order_estimated_delivery_date
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_estimated_delivery_date IS NOT NULL
              AND date(order_delivered_customer_date) > date(order_estimated_delivery_date);
        """
    },

    # =========================
    # Payment Reconciliation Checks
    # =========================
    {
        "check_category": "payment_reconciliation",
        "check_name": "payment_total_not_equal_item_total",
        "severity": "WARNING",
        "query": """
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
            WHERE ABS(ROUND(p.total_payment_value - i.total_item_value, 2)) > 0.01;
        """
    }
]
