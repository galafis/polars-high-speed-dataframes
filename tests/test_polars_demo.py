import unittest
import sys
import os
import polars as pl
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.polars_demo import PolarsDataProcessor

class TestPolarsDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PolarsDataProcessor()
        self.data = {
            "first_name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"],
            "last_name": ["Smith", "Jones", "Brown", "Wilson", "Davis", "Miller", "Moore", "Taylor"],
            "age": [25, 30, 35, 28, 40, 22, 32, 45],
            "city": ["New York", "London", "New York", "Paris", "London", "New York", "Paris", "London"],
            "monthly_salary": [50000, 70000, 60000, 55000, 80000, 45000, 65000, 90000]
        }
        self.df = pl.DataFrame(self.data)
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_data_from_dict(self):
        """Test loading data from dictionary."""
        result = self.processor.load_data_from_dict(self.data)
        self.assertIsInstance(result, pl.DataFrame)
        self.assertEqual(result.shape[0], 8)
        self.assertIn("first_name", result.columns)

    def test_read_write_csv(self):
        """Test CSV read and write operations."""
        csv_file = os.path.join(self.test_dir, "test_data.csv")
        self.processor.write_csv(self.df, csv_file)
        self.assertTrue(os.path.exists(csv_file))
        read_df = self.processor.read_csv(csv_file)
        self.assertEqual(read_df.shape, self.df.shape)

    def test_read_write_parquet(self):
        """Test Parquet read and write operations."""
        parquet_file = os.path.join(self.test_dir, "test_data.parquet")
        self.processor.write_parquet(self.df, parquet_file)
        self.assertTrue(os.path.exists(parquet_file))
        read_df = self.processor.read_parquet(parquet_file)
        self.assertEqual(read_df.shape, self.df.shape)

    def test_filter_by_condition(self):
        """Test filtering DataFrame by condition."""
        filtered_df = self.processor.filter_by_condition(self.df, pl.col("age") > 30)
        self.assertIsInstance(filtered_df, pl.DataFrame)
        self.assertTrue(all(filtered_df["age"] > 30))
        self.assertEqual(filtered_df.shape[0], 4)  # Charlie, Eve, Grace, Heidi

    def test_calculate_summary_statistics(self):
        """Test calculation of summary statistics."""
        summary_df = self.processor.calculate_summary_statistics(self.df, "city", "age")
        self.assertIsInstance(summary_df, pl.DataFrame)
        self.assertIn("mean_age", summary_df.columns)
        self.assertIn("median_age", summary_df.columns)
        self.assertIn("min_age", summary_df.columns)
        self.assertIn("max_age", summary_df.columns)
        self.assertIn("std_age", summary_df.columns)
        self.assertIn("count", summary_df.columns)
        
        # Check New York stats (Alice, Charlie, Frank: ages 25, 35, 22)
        ny_stats = summary_df.filter(pl.col("city") == "New York")
        self.assertEqual(ny_stats.shape[0], 1)
        self.assertAlmostEqual(ny_stats["mean_age"].item(), (25 + 35 + 22) / 3, places=1)

    def test_add_derived_columns(self):
        """Test adding derived columns."""
        df_with_derived = self.processor.add_derived_columns(self.df)
        self.assertIsInstance(df_with_derived, pl.DataFrame)
        self.assertIn("full_name", df_with_derived.columns)
        self.assertIn("age_group", df_with_derived.columns)
        self.assertIn("annual_salary", df_with_derived.columns)
        
        # Check full name concatenation
        alice_row = df_with_derived.filter(pl.col("first_name") == "Alice")
        self.assertEqual(alice_row["full_name"].item(), "Alice Smith")
        
        # Check age group categorization
        self.assertEqual(alice_row["age_group"].item(), "Young")
        heidi_row = df_with_derived.filter(pl.col("first_name") == "Heidi")
        # Heidi is 45, which is Adult (30-50)
        self.assertEqual(heidi_row["age_group"].item(), "Adult")

    def test_apply_window_function(self):
        """Test applying window functions."""
        df_with_window = self.processor.apply_window_function(self.df, "city", "age", "monthly_salary")
        self.assertIsInstance(df_with_window, pl.DataFrame)
        self.assertIn("rolling_mean_monthly_salary", df_with_window.columns)
        self.assertIn("rank_monthly_salary", df_with_window.columns)

    def test_handle_missing_data_mean(self):
        """Test handling missing data with mean strategy."""
        # Create data with null values
        data_with_nulls = self.data.copy()
        data_with_nulls["monthly_salary"] = [50000, None, 60000, 55000, None, 45000, 65000, 90000]
        df_nulls = pl.DataFrame(data_with_nulls)
        
        result = self.processor.handle_missing_data(df_nulls, strategy="mean", column="monthly_salary")
        self.assertEqual(result["monthly_salary"].null_count(), 0)

    def test_handle_missing_data_drop(self):
        """Test handling missing data by dropping nulls."""
        data_with_nulls = self.data.copy()
        data_with_nulls["monthly_salary"] = [50000, None, 60000, 55000, None, 45000, 65000, 90000]
        df_nulls = pl.DataFrame(data_with_nulls)
        
        result = self.processor.handle_missing_data(df_nulls, strategy="drop", column="monthly_salary")
        self.assertEqual(result.shape[0], 6)  # 2 rows dropped

    def test_perform_join(self):
        """Test join operations between DataFrames."""
        other_data = {
            "first_name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "department": ["HR", "Engineering", "Sales", "Marketing", "Engineering"]
        }
        other_df = pl.DataFrame(other_data)
        
        joined_df = self.processor.perform_join(self.df, other_df, "first_name", how="inner")
        self.assertIsInstance(joined_df, pl.DataFrame)
        self.assertIn("department", joined_df.columns)
        self.assertEqual(joined_df.shape[0], 5)
        
        alice_dept = joined_df.filter(pl.col("first_name") == "Alice")["department"].item()
        self.assertEqual(alice_dept, "HR")

    def test_execute_sql_query(self):
        """Test SQL query execution on DataFrames."""
        df_map = {"employees": self.df}
        query = "SELECT first_name, last_name, age FROM employees WHERE age > 30 ORDER BY age"
        
        result = self.processor.execute_sql_query(df_map, query)
        self.assertIsInstance(result, pl.DataFrame)
        self.assertEqual(result.shape[0], 4)  # Charlie, Eve, Grace, Heidi
        self.assertTrue(all(result["age"] > 30))

if __name__ == '__main__':
    unittest.main(verbosity=2)

