import unittest
import sys
import os
import polars as pl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from polars_demo import PolarsProcessor

class TestPolarsProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PolarsProcessor()
        self.data = {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"],
            "age": [25, 30, 35, 28, 40, 22, 32, 45],
            "city": ["New York", "London", "New York", "Paris", "London", "New York", "Paris", "London"],
            "salary": [50000, 70000, 60000, 55000, 80000, 45000, 65000, 90000]
        }
        self.df = pl.DataFrame(self.data)
        self.test_dir = "./test_data"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for f in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, f))
            os.rmdir(self.test_dir)

    def test_group_and_aggregate(self):
        avg_salary_df = self.processor.group_and_aggregate(self.df)
        self.assertIsInstance(avg_salary_df, pl.DataFrame)
        self.assertEqual(avg_salary_df.shape, (4, 2))
        self.assertIn("city", avg_salary_df.columns)
        self.assertIn("avg_salary", avg_salary_df.columns)
        self.assertAlmostEqual(avg_salary_df.filter(pl.col("city") == "New York")["avg_salary"].item(), (50000 + 60000 + 45000)/3)

    def test_add_bonus_column(self):
        df_with_bonus = self.processor.add_bonus_column(self.df, 0.10)
        self.assertIsInstance(df_with_bonus, pl.DataFrame)
        self.assertIn("bonus_salary", df_with_bonus.columns)
        self.assertEqual(df_with_bonus.filter(pl.col("name") == "Alice")["bonus_salary"].item(), 50000 * 1.10)

    def test_chain_operations(self):
        chained_df = self.processor.chain_operations(self.df, 25, 0.05)
        self.assertIsInstance(chained_df, pl.DataFrame)
        self.assertTrue(all(chained_df["age"] > 25))
        self.assertIn("bonus_salary", chained_df.columns)
        self.assertEqual(chained_df.shape, (7, 5)) # Alice (25) is filtered out

    def test_complex_lazy_evaluation(self):
        complex_lazy_df = self.processor.complex_lazy_evaluation(self.df, 25, 60000)
        self.assertIsInstance(complex_lazy_df, pl.DataFrame)
        self.assertTrue(all(complex_lazy_df["age"] > 25))
        self.assertTrue(all(complex_lazy_df["avg_salary_city"] < 60000))
        self.assertEqual(complex_lazy_df.shape, (3, 5)) # Bob, David, Grace

    def test_join_with_another_dataframe(self):
        other_data = {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "department": ["HR", "Engineering", "Sales", "Marketing", "Engineering"]
        }
        other_df = pl.DataFrame(other_data)
        joined_df = self.processor.join_with_another_dataframe(self.df, other_df, "name")
        self.assertIsInstance(joined_df, pl.DataFrame)
        self.assertIn("department", joined_df.columns)
        self.assertEqual(joined_df.shape, (5, 5))
        self.assertEqual(joined_df.filter(pl.col("name") == "Alice")["department"].item(), "HR")

    def test_calculate_correlation(self):
        correlation = self.processor.calculate_correlation(self.df, "age", "salary")
        self.assertIsInstance(correlation, float)
        # Since the data is somewhat correlated, check if it's not zero
        self.assertNotAlmostEqual(correlation, 0.0)

    def test_read_write_csv_file(self):
        csv_file = os.path.join(self.test_dir, "test_data.csv")
        self.df.write_csv(csv_file)
        self.assertTrue(os.path.exists(csv_file))
        read_df = self.processor.read_csv_file(csv_file)
        self.assertTrue(self.df.frame_equal(read_df))

    def test_read_write_parquet_file(self):
        parquet_file = os.path.join(self.test_dir, "test_data.parquet")
        self.df.write_parquet(parquet_file)
        self.assertTrue(os.path.exists(parquet_file))
        read_df = self.processor.read_parquet_file(parquet_file)
        self.assertTrue(self.df.frame_equal(read_df))

if __name__ == '__main__':
    unittest.main(verbosity=2)

