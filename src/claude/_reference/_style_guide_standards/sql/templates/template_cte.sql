with

import_orders as (
    -- query only non-test orders
    select * from {{ source('jaffle_shop', 'orders') }}
    where amount > 0
),

import_customers as (
    select * from {{ source('jaffle_shop', 'customers') }}
),

logical_cte_1 as (

    -- perform some math on import_orders

),

logical_cte_2 as (

    -- perform some math on import_customers
),

final_cte as (

    -- join together logical_cte_1 and logical_cte_2
)

SELECT * FROM final_cte
