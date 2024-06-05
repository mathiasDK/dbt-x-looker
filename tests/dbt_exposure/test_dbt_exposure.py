from src.dbt_exposure.dbt_exposure import dbtLookerExposure
import unittest
import os

class TestDbtLookerExposure(unittest.TestCase):

    def setUp(self):
        main_path = os.getcwd()
        self.looker_path = f"{main_path}/test_data/looker"
        self.dbt_path = f"{main_path}/test_data/dbt"
        self.exposure = dbtLookerExposure(self.looker_path, self.dbt_path)

    def test_initialization(self):
        self.assertEqual(self.exposure.looker_path, self.looker_path)
        self.assertEqual(self.exposure.dbt_path, self.dbt_path)

    def test_update_looker_path(self):
        new_path = "new/path/to/looker"
        self.exposure.update_looker_path = new_path
        self.assertEqual(self.exposure.looker_path, new_path)

    def test_update_dbt_path(self):
        new_path = "new/path/to/dbt"
        self.exposure.update_dbt_path = new_path
        self.assertEqual(self.exposure.dbt_path, new_path)

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
        actuals = {"sales_explore": ["dim_customer", "dim_store", "fct_sales"]}
        extracted = self.exposure.get_all_exposure_tables()
        print("="*40)
        print(extracted)
        print("="*40)
        self.assertEqual(actuals, extracted)

    def test_get_exposure_tables(self):
        exposure_name = "sales_explore"
        actuals = ["dim_customer", "dim_store", "fct_sales"].sort()
        extracted = self.exposure.get_exposure_tables(exposure_name=exposure_name).sort()
        self.assertEqual(actuals, extracted)

    def test_get_table_columns(self):
        views = ["dim_customer", "dim_store", "fct_sales"]
        actuals = {
            "dim_customer": ["customer_id", "name", "market", "signed_up_at", "first_purchase_at", "segment", "updated_at"],
            "dim_store": ["store_id", "name", "segment", "area", "store_version"],
            "fct_sales": ["order_id", "store_id", "customer_id", "order_date", "shipping_date", "revenue", "is_large_order", "cost", "margin"]
        }
        for view in views:
            extracted = self.exposure.get_table_columns(table_name=view)
            self.assertEqual(actuals.get(view).sort(), extracted.sort())

    def test_get_table_sql_columns(self):
        views = ["dim_customer", "dim_store", "fct_sales"]
        actuals = {
            "dim_customer": ["customer_id", "name", "market", "signed_up_at", "first_purchase_at", "segment", "updated_at"],
            "dim_store": ["store_id", "name", "store_segment", "area", "store_version"],
            "fct_sales": ["order_id", "store_id", "customer_id", "order_date", "shipping_date", "revenue", "is_large_order", "cost", "margin"]
        }
        for view in views:
            extracted = self.exposure.get_table_sql_columns(table_name=view)
            self.assertEqual(actuals.get(view).sort(), extracted.sort())

    def test_create_exposure_doc(self):
        with self.assertRaises(NotImplementedError):
            self.exposure.create_exposure_doc("example_exposure")

    def test_create_all_exposures_docs(self):
        with self.assertRaises(NotImplementedError):
            self.exposure.create_all_exposures_docs()

    def test_update_exposure_doc(self):
        with self.assertRaises(NotImplementedError):
            self.exposure.update_exposure_doc("example_content")

if __name__ == '__main__':
    unittest.main()
