view: customer {
  sql_table_name: sales_mart.dim_customer ;;  # The actual table name in your database
  label: "Customer"

  dimension: customer_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.customer_id ;;
    hidden: yes 
  }

  dimension: name {
    type: string
    description: "The full name of the customer."
    sql: ${TABLE}.name ;;
  }

  dimension: market {
    type: string
    description: "The market in which the customer is located."
    sql: ${TABLE}.market ;;
  }

  dimension: signed_up_at {
    type: string
    description: "The date and time when the customer signed up."
    sql: ${TABLE}.signed_up_at ;;
  }

  dimension: first_purchase_at {
    type: string
    description: "The date and time when the customer made their first purchase."
    sql: ${TABLE}.first_purchase_at ;;
  }

  dimension: segment {
    type: timestamp
    description: "The segment or category to which the customer belongs."
    sql: ${TABLE}.segment ;;
  }

  dimension: updated_at {
    type: timestamp
    sql: ${TABLE}.updated_at ;;
  }

  measure: n_customers {
    label: "# of Customers"
    type: count_distinct
    sql: ${TABLE}.customer_id ;;
  }
}
