{{ config(
    materialized='table',
    schema='sales_mart',
    tags=['dimension', 'sales_mart']
) }}

select
    customer_id,
    name,
    market,
    signed_up_at,
    first_purchase_at,
    segment
from {{ ref('stg_customers') }}
