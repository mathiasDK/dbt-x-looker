from src.dbt_exposure.dbt_exposure import LookerContentExtractor
import unittest
import os
import re

class TestLookerContentExtractor(unittest.TestCase):

    def setUp(self):
        main_path = os.getcwd()
        self.looker_path = f"{main_path}/test_data/looker"
        self.exposure = LookerContentExtractor(self.looker_path)

    def test_initialization(self):
        self.assertEqual(self.exposure.looker_path, self.looker_path)

    def test_get_exposure_files(self):
        actuals = [f"{self.exposure.looker_path}/models/sales.model.lkml"]
        extracted = self.exposure._get_exposure_files()
        self.assertEqual(actuals, extracted, msg=f"Exposure files\nActual: {actuals},\nExtracted: {extracted}")

    def test_get_view_files(self):
        actuals = [
            f"{self.exposure.looker_path}/views/sales_mart/dim_customer.view.lkml",
            f"{self.exposure.looker_path}/views/sales_mart/dim_store.view.lkml",
            f"{self.exposure.looker_path}/views/sales_mart/fct_sales.view.lkml",
        ]
        extracted = self.exposure._get_view_files()
        self.assertEqual(actuals, extracted)

    def test_get_all_exposure_tables(self):
        actuals = {"sales_explore": ["fact_sales", "customer", "dim_store"]}
        extracted = self.exposure.get_all_exposure_tables()
        self.assertEqual(actuals, extracted)

    def test_get_exposure_tables(self):
        if self.exposure.exposure_to_tables is None:
            self.exposure.get_all_exposure_tables()
        exposure_name = "sales_explore"
        actuals = ["fact_sales", "customer", "dim_store"]
        extracted = self.exposure.get_exposure_tables(exposure_name=exposure_name)
        self.assertEqual(actuals, extracted)

    def test_get_all_matches(self):
        s = """
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
        """
        pattern_explore = r'explore:\s*(\w+)'
        pattern_from = r'from:\s*(\w+)'
        pattern_join = r'join:\s*(\w+)'

        self.assertEqual(["sales_explore"], self.exposure._get_all_matches(s, pattern_explore))
        self.assertEqual(["fact_sales"], self.exposure._get_all_matches(s, pattern_from))
        self.assertEqual(["customer", "dim_store"], self.exposure._get_all_matches(s, pattern_join))

    def test_extract_table_sql_columns(self):
        s = """
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
                type: string
                description: "The segment or category to which the customer belongs."
                sql: ${TABLE}.segment ;;
            }

            dimension: segment_market {
                type: string
                description: "The segment or category to which the customer belongs."
                sql: ${TABLE}.segment || ${TABLE}.market ;;
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
            """
        actuals = ['customer_id', 'first_purchase_at', 'market', 'name', 'segment', 'signed_up_at', 'updated_at']
        extracted = self.exposure._extract_table_sql_columns(s)
        self.assertEqual(actuals, extracted)

    def test_extract_sql_tables_derived_table(self):
        s = """
        view: fact_sales {
            label: "Sales Data"  # Grouping under Sales Data in the Looker UI

            derived_table: {
                sql: SELECT
                    order_id,
                    store_id,
                    customer_id,
                    order_date,
                    shipping_date,
                    revenue,
                    cost,
                    margin
                    FROM sales_mart.fct_sales_west
                    
                    UNION ALL
                    
                    SELECT
                    order_id,
                    store_id,
                    customer_id,
                    order_date,
                    shipping_date,
                    revenue,
                    cost,
                    margin
                    FROM sales_mart.fct_sales_east 
                    ;;
            }

            dimension: order_id {
                primary_key: yes
                type: string
                sql: ${TABLE}.order_id ;;
                hidden: yes
            }
        }
        """
        actuals = ["sales_mart.fct_sales_west", "sales_mart.fct_sales_east"]
        extracted = self.exposure._extract_sql_tables(s)
        self.assertEqual(actuals, extracted)

    def test_extract_sql_tables_simple(self):
        s = """
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
        }
        """
        actuals = ["sales_mart.dim_customer"]
        extracted = self.exposure._extract_sql_tables(s)
        self.assertEqual(actuals, extracted)

    # def test_get_table_sql_columns(self):
    #     views = ["dim_customer", "dim_store", "fct_sales"]
    #     actuals = {
    #         "dim_customer": ["customer_id", "name", "market", "signed_up_at", "first_purchase_at", "segment", "updated_at"],
    #         "dim_store": ["store_id", "name", "store_segment", "area", "store_version"],
    #         "fct_sales": ["order_id", "store_id", "customer_id", "order_date", "shipping_date", "revenue", "is_large_order", "cost", "margin"]
    #     }
    #     for view in views:
    #         extracted = self.exposure.get_table_sql_columns(table_name=view)
    #         self.assertEqual(actuals.get(view).sort(), extracted.sort())

if __name__ == '__main__':
    unittest.main()
