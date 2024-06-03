{{ config(
    materialized='table',
    schema='sales_mart',
    tags=['fact', 'sales_mart']
) }}

select
    order_id,
    store_id,
    customer_id,
    order_date,
    shipping_date,
    revenue,
    cost,
    revenue - cost as margin
from {{ ref('stg_sales') }}
