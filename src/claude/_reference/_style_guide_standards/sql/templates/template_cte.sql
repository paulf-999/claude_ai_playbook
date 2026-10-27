WITH

import_orders AS (
    -- query only non-test orders
    SELECT
        order_id
        , customer_id
        , amount
    FROM {{ source('jaffle_shop', 'orders') }}
    WHERE amount > 0
),

import_customers AS (
    SELECT
        customer_id
        , first_name
        , last_name
    FROM {{ source('jaffle_shop', 'customers') }}
),

logical_cte_1 AS (
    -- perform some math on import_orders
),

logical_cte_2 AS (
    -- perform some math on import_customers
),

final_cte AS (
    -- join together logical_cte_1 and logical_cte_2
)

SELECT
    -- list the final columns explicitly
FROM final_cte
