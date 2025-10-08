
"""
Polars High-Speed DataFrames
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra o uso do Polars para processamento de dados em alta velocidade.
"""

import polars as pl
from typing import Dict, Any

class PolarsDataProcessor:
    """
    Classe para demonstrar operações de processamento de dados com Polars.
    """

    def load_data(self, data: Dict[str, Any]) -> pl.DataFrame:
        """Carrega dados de um dicionário para um DataFrame Polars."""
        return pl.DataFrame(data)

    def filter_by_age(self, df: pl.DataFrame, min_age: int) -> pl.DataFrame:
        """Filtra o DataFrame por idade mínima."""
        return df.filter(pl.col("age") > min_age)

    def calculate_average_salary_by_city(self, df: pl.DataFrame) -> pl.DataFrame:
        """Calcula a média salarial por cidade."""
        return df.group_by("city").agg(pl.col("salary").mean().alias("avg_salary"))

    def add_bonus_column(self, df: pl.DataFrame, bonus_rate: float) -> pl.DataFrame:
        """Adiciona uma coluna de bônus baseada no salário."""
        return df.with_columns((pl.col("salary") * bonus_rate).alias("bonus"))

    def chain_operations(self, df: pl.DataFrame, min_age: int, bonus_rate: float) -> pl.DataFrame:
        """Encadeia múltiplas operações de processamento de dados."""
        return (
            df.lazy()
            .filter(pl.col("age") > min_age)
            .with_columns((pl.col("salary") * bonus_rate).alias("bonus"))
            .collect()
        )


if __name__ == "__main__":
    print("=" * 60)
    print("Polars High-Speed DataFrames Demo")
    print("=" * 60)

    processor = PolarsDataProcessor()
    data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "name": [f"User{i}" for i in range(1, 11)],
        "age": [24, 27, 22, 32, 29, 35, 28, 40, 21, 30],
        "city": ["NY", "LA", "NY", "SF", "LA", "NY", "SF", "LA", "NY", "SF"],
        "salary": [50000, 60000, 45000, 75000, 62000, 80000, 55000, 90000, 40000, 70000]
    }
    df = processor.load_data(data)
    print("\nOriginal DataFrame:")
    print(df)

    print("\nFiltered by age > 25:")
    filtered_df = processor.filter_by_age(df, 25)
    print(filtered_df)

    print("\nAverage salary by city:")
    avg_salary_df = processor.calculate_average_salary_by_city(df)
    print(avg_salary_df)

    print("\nDataFrame with bonus (10%):")
    df_with_bonus = processor.add_bonus_column(df, 0.10)
    print(df_with_bonus)

    print("\nChained operations (age > 25, 5% bonus):")
    chained_df = processor.chain_operations(df, 25, 0.05)
    print(chained_df)

