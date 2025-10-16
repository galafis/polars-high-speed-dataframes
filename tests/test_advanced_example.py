import unittest
import sys
import os
import polars as pl
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from examples.advanced_example import AdvancedPolarsProcessor


class TestAdvancedPolarsProcessor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.processor = AdvancedPolarsProcessor()
        # Override data directory to use temp directory
        self.processor.data_dir = self.test_dir

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_sample_data(self):
        """Test creation of sample sales and customer data."""
        sales_df, customer_df = self.processor.create_sample_data()
        
        # Check sales DataFrame
        self.assertIsInstance(sales_df, pl.DataFrame)
        self.assertEqual(sales_df.shape[0], 1000)
        self.assertIn("order_id", sales_df.columns)
        self.assertIn("product", sales_df.columns)
        self.assertIn("category", sales_df.columns)
        self.assertIn("price", sales_df.columns)
        self.assertIn("quantity", sales_df.columns)
        self.assertIn("customer_id", sales_df.columns)
        self.assertIn("order_date", sales_df.columns)
        
        # Check customer DataFrame
        self.assertIsInstance(customer_df, pl.DataFrame)
        self.assertEqual(customer_df.shape[0], 100)
        self.assertIn("customer_id", customer_df.columns)
        self.assertIn("region", customer_df.columns)
        self.assertIn("loyalty_status", customer_df.columns)
        
        # Check files were created
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "sales_data.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "customer_data.parquet")))

    def test_load_data(self):
        """Test loading data from files."""
        # First create the data
        self.processor.create_sample_data()
        
        # Then load it
        sales_df, customer_df = self.processor.load_data()
        
        self.assertIsInstance(sales_df, pl.DataFrame)
        self.assertIsInstance(customer_df, pl.DataFrame)
        self.assertEqual(sales_df.shape[0], 1000)
        self.assertEqual(customer_df.shape[0], 100)

    def test_process_sales_data(self):
        """Test processing of sales data with joins and aggregations."""
        sales_df, customer_df = self.processor.create_sample_data()
        
        sales_summary, top_customers, daily_sales = self.processor.process_sales_data(
            sales_df, customer_df
        )
        
        # Check sales summary
        self.assertIsInstance(sales_summary, pl.DataFrame)
        self.assertIn("category", sales_summary.columns)
        self.assertIn("region", sales_summary.columns)
        self.assertIn("total_revenue", sales_summary.columns)
        self.assertIn("number_of_orders", sales_summary.columns)
        self.assertIn("avg_quantity_per_order", sales_summary.columns)
        
        # Check top customers
        self.assertIsInstance(top_customers, pl.DataFrame)
        self.assertEqual(top_customers.shape[0], 5)
        self.assertIn("customer_id", top_customers.columns)
        self.assertIn("total_spent", top_customers.columns)
        # Verify it's sorted descending by total_spent
        total_spent_list = top_customers["total_spent"].to_list()
        self.assertEqual(total_spent_list, sorted(total_spent_list, reverse=True))
        
        # Check daily sales
        self.assertIsInstance(daily_sales, pl.DataFrame)
        self.assertIn("day", daily_sales.columns)
        self.assertIn("daily_revenue", daily_sales.columns)
        # Verify it's sorted by day
        self.assertTrue(daily_sales["day"].is_sorted())

    def test_sales_summary_aggregations(self):
        """Test that sales summary performs correct aggregations."""
        sales_df, customer_df = self.processor.create_sample_data()
        sales_summary, _, _ = self.processor.process_sales_data(sales_df, customer_df)
        
        # Check that all aggregation columns exist and have valid values
        self.assertTrue(all(sales_summary["total_revenue"] >= 0))
        self.assertTrue(all(sales_summary["number_of_orders"] > 0))
        self.assertTrue(all(sales_summary["avg_quantity_per_order"] > 0))

    def test_data_consistency(self):
        """Test data consistency between sales and customer data."""
        sales_df, customer_df = self.processor.create_sample_data()
        
        # Check that all customer_ids in sales exist in customer data
        unique_sales_customers = sales_df["customer_id"].unique().sort()
        unique_customers = customer_df["customer_id"].unique().sort()
        
        # All sales customers should be in customer data
        sales_customer_set = set(unique_sales_customers.to_list())
        customer_set = set(unique_customers.to_list())
        self.assertTrue(sales_customer_set.issubset(customer_set))


if __name__ == '__main__':
    unittest.main(verbosity=2)
