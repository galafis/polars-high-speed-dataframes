
import unittest
import sys
import os
import polars as pl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from polars_demo import PolarsDataProcessor

class TestPolarsDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PolarsDataProcessor()
        self.data = {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [24, 27, 22, 32, 29],
            "city": ["NY", "LA", "NY", "SF", "LA"],
            "salary": [50000, 60000, 45000, 75000, 62000]
        }
        self.df = pl.DataFrame(self.data)

    def test_load_data(self):
        # Testar se o método load_data retorna um DataFrame Polars
        loaded_df = self.processor.load_data(self.data)
        self.assertIsInstance(loaded_df, pl.DataFrame)
        self.assertEqual(loaded_df.shape, (5, 5))

    def test_filter_by_age(self):
        # Testar a filtragem por idade
        filtered_df = self.processor.filter_by_age(self.df, 25)
        self.assertEqual(filtered_df.shape, (3, 5))
        self.assertTrue(all(filtered_df["age"] > 25))

    def test_calculate_average_salary_by_city(self):
        # Testar o cálculo da média salarial por cidade
        avg_salary_df = self.processor.calculate_average_salary_by_city(self.df)
        self.assertIsInstance(avg_salary_df, pl.DataFrame)
        self.assertEqual(avg_salary_df.shape, (3, 2))
        self.assertIn("city", avg_salary_df.columns)
        self.assertIn("avg_salary", avg_salary_df.columns)
        self.assertAlmostEqual(avg_salary_df.filter(pl.col("city") == "NY")["avg_salary"].item(), 47500.0)

    def test_add_bonus_column(self):
        # Testar a adição de uma coluna de bônus
        df_with_bonus = self.processor.add_bonus_column(self.df, 0.10)
        self.assertIn("bonus", df_with_bonus.columns)
        self.assertEqual(df_with_bonus["bonus"].sum(), self.df["salary"].sum() * 0.10)

    def test_chain_operations(self):
        # Testar o encadeamento de operações
        result_df = self.processor.chain_operations(self.df, 25, 0.05)
        self.assertIsInstance(result_df, pl.DataFrame)
        self.assertEqual(result_df.shape, (3, 6)) # 3 linhas, 5 colunas originais + 1 bônus
        self.assertTrue(all(result_df["age"] > 25))
        self.assertIn("bonus", result_df.columns)

if __name__ == '__main__':
    unittest.main(verbosity=2)

