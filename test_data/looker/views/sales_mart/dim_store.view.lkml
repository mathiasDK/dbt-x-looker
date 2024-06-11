# views/dim_customer.view.lkml

view: dim_store {
  sql_table_name: sales_mart.dim_store ;;  # The actual table name in your database
  label: "Store"

  dimension: store_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.store_id ;;
    hidden: yes 
  }

  dimension: name {
    type: string
    sql: ${TABLE}.name ;;
  }

  dimension: segment {
    type: string
    sql: ${TABLE}.store_segment ;;
  }

  dimension: area {
    type: string
    sql: ${TABLE}.area ;;
  }

  dimension: store_version {
    type: string
    sql: ${TABLE}.store_version ;;
  }

  measure: n_stores {
    label: "# of Stores"
    type: count_distinct
    sql: ${TABLE}.store_id ;;
  }
}
