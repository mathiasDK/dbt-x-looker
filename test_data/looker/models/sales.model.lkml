connection: "prod"

explore: sales_explore {
  label: "Sales"
  from: fact_sales

  join: customer {
    sql_on: ${fact_sales.customer_id} = ${customer.customer_id} ;;
    relationship: many_to_one
  }

  join: dim_store {
    sql_on: ${fact_sales.store_id} = ${dim_store.store_id} ;;
    relationship: many_to_one
  }
}
