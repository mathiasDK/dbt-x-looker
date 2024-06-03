# views/fact_sales.view.lkml

view: fact_sales {
  label: "Sales Data"  # Grouping under Sales Data in the Looker UI

  sql_table_name: sales_mart.fact_sales ;;  # The actual table name in your database

  dimension: order_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.order_id ;;
    hidden: yes
  }

  dimension: store_id {
    hidden: yes
    type: string
    sql: ${TABLE}.store_id ;;
  }

  dimension: customer_id {
    hidden: yes
    type: string
    sql: ${TABLE}.customer_id ;;
  }

  dimension_group: order_date {
    type: date
    timeframes: [date, week, month, raw]
    sql: ${TABLE}.order_date ;;
  }

  dimension_group: shipping_date {
    type: date
    timeframes: [date, week, month, raw]
    sql: ${TABLE}.shipping_date ;;
  }

  dimension: revenue {
    type: number
    sql: ${TABLE}.revenue ;;
    value_format:"$#.00;($#.00)"
  }

  dimension: cost {
    type: number
    sql: ${TABLE}.cost ;;
    value_format:"$#.00;($#.00)"
  }

  dimension: margin {
    type: number
    sql: ${TABLE}.margin ;;
    value_format:"$#.00;($#.00)"
    description: "Revenue minus cost, representing the margin."
  }

  measure: total_revenue {
    type: sum
    sql: ${revenue} ;;
    value_format:"$#.00;($#.00)"
    description: "Total revenue from sales."
  }

  measure: total_cost {
    type: sum
    sql: ${cost} ;;
    value_format:"$#.00;($#.00)"
    description: "Total cost of sales."
  }

  measure: total_margin {
    type: sum
    sql: ${margin} ;;
    value_format:"$#.00;($#.00)"
    description: "Total margin from sales."
  }

  measure: average_margin {
    type: average
    sql: ${margin} ;;
    value_format:"$#.00;($#.00)"
    description: "Average margin per order."
  }

  measure: n_orders {
    type: count_distinct
    sql: ${TABLE}.order_id ;;
    description: "Count of sales orders."
  }
}
