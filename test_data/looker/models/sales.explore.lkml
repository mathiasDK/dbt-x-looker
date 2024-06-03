explore: sales_explore {
  label: "Sales Explore"
  from: fact_sales

  join: dim_customer {
    sql_on: ${fact_sales.customer_id} = ${dim_customer.customer_id} ;;
    relationship: many_to_one
  }

  join: dim_store {
    sql_on: ${fact_sales.store_id} = ${dim_store.store_id} ;;
    relationship: many_to_one
  }
}
