{{ config(
    materialized='table',
    schema='sales_mart',
    tags=['dimension', 'sales_mart']
) }}

select
    store_id,
    name,
    area,
    store_version
from {{ ref('stg_store') }}
