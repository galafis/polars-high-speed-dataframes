
"""
Polars High-Speed DataFrames
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo demonstra o uso do Polars para processamento de dados em alta velocidade,
com funcionalidades aprimoradas para leitura/escrita de arquivos, transformações complexas
e uso de expressões avançadas.
"""

import polars as pl
from typing import Dict, Any, List, Optional
import os

class PolarsDataProcessor:
    """
    Classe para demonstrar operações de processamento de dados com Polars.
    """

    def load_data_from_dict(self, data: Dict[str, Any]) -> pl.DataFrame:
        """Carrega dados de um dicionário para um DataFrame Polars."""
        return pl.DataFrame(data)

    def read_csv(self, file_path: str, **kwargs) -> pl.DataFrame:
        """Lê dados de um arquivo CSV para um DataFrame Polars."""
        return pl.read_csv(file_path, **kwargs)

    def write_csv(self, df: pl.DataFrame, file_path: str, **kwargs):
        """Escreve um DataFrame Polars para um arquivo CSV."""
        df.write_csv(file_path, **kwargs)
        print(f"✓ DataFrame escrito para CSV: {file_path}")

    def read_parquet(self, file_path: str, **kwargs) -> pl.DataFrame:
        """Lê dados de um arquivo Parquet para um DataFrame Polars."""
        return pl.read_parquet(file_path, **kwargs)

    def write_parquet(self, df: pl.DataFrame, file_path: str, **kwargs):
        """Escreve um DataFrame Polars para um arquivo Parquet."""
        df.write_parquet(file_path, **kwargs)
        print(f"✓ DataFrame escrito para Parquet: {file_path}")

    def filter_by_condition(self, df: pl.DataFrame, condition: pl.Expr) -> pl.DataFrame:
        """Filtra o DataFrame usando uma expressão Polars."""
        return df.filter(condition)

    def calculate_summary_statistics(self, df: pl.DataFrame, group_col: str, agg_col: str) -> pl.DataFrame:
        """
        Calcula estatísticas de resumo (média, mediana, min, max, desvio padrão)
        agrupadas por uma coluna.
        """
        return df.group_by(group_col).agg(
            pl.col(agg_col).mean().alias(f"mean_{agg_col}"),
            pl.col(agg_col).median().alias(f"median_{agg_col}"),
            pl.col(agg_col).min().alias(f"min_{agg_col}"),
            pl.col(agg_col).max().alias(f"max_{agg_col}"),
            pl.col(agg_col).std().alias(f"std_{agg_col}"),
            pl.len().alias("count")
        ).sort(group_col)

    def add_derived_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Adiciona colunas derivadas usando expressões Polars, como:
        - `full_name`: Concatenação de nome e sobrenome.
        - `age_group`: Categorização da idade.
        - `salary_per_year`: Salário anual (se houver salário mensal).
        """
        return df.with_columns(
            (pl.col("first_name") + pl.lit(" ") + pl.col("last_name")).alias("full_name"),
            pl.when(pl.col("age") < 30).then(pl.lit("Young"))
            .when(pl.col("age") < 50).then(pl.lit("Adult"))
            .otherwise(pl.lit("Senior")).alias("age_group"),
            (pl.col("monthly_salary") * 12).fill_null(0).alias("annual_salary")
        )

    def apply_window_function(self, df: pl.DataFrame, partition_col: str, order_col: str, target_col: str) -> pl.DataFrame:
        """
        Aplica uma função de janela (ex: média móvel, rank) a um DataFrame.
        Calcula a média móvel de `target_col` particionada por `partition_col` e ordenada por `order_col`.
        """
        return df.with_columns(
            pl.col(target_col).rolling_mean(window_size=2).over(partition_col).alias(f"rolling_mean_{target_col}"),
            pl.col(target_col).rank().over(partition_col).alias(f"rank_{target_col}")
        ).sort(partition_col, order_col)

    def handle_missing_data(self, df: pl.DataFrame, strategy: str = "mean", column: str = None) -> pl.DataFrame:
        """
        Lida com dados ausentes usando diferentes estratégias (média, mediana, moda, preenchimento com valor).
        """
        if column is None:
            print("Aviso: Nenhuma coluna especificada para tratamento de nulos. Retornando DataFrame original.")
            return df

        if strategy == "mean":
            mean_val = df.select(pl.col(column).mean()).item()
            return df.fill_null(mean_val)
        elif strategy == "median":
            median_val = df.select(pl.col(column).median()).item()
            return df.fill_null(median_val)
        elif strategy == "mode":
            # Polars não tem um método direto para moda, mas pode ser feito com value_counts
            mode_val = df.group_by(column).len().sort(pl.col("len"), descending=True).select(pl.col(column)).item()
            return df.fill_null(mode_val)
        elif strategy == "forward_fill":
            return df.fill_null(strategy="forward")
        elif strategy == "backward_fill":
            return df.fill_null(strategy="backward")
        elif strategy == "drop":
            return df.drop_nulls(subset=[column])
        else:
            print(f"Estratégia de tratamento de nulos desconhecida: {strategy}. Retornando DataFrame original.")
            return df

    def perform_join(self, df1: pl.DataFrame, df2: pl.DataFrame, on_col: str, how: str = "inner") -> pl.DataFrame:
        """
        Realiza um join entre dois DataFrames.
        """
        return df1.join(df2, on=on_col, how=how)

    def execute_sql_query(self, df_map: Dict[str, pl.DataFrame], query: str) -> pl.DataFrame:
        """
        Executa uma query SQL diretamente em DataFrames Polars usando o contexto SQL.
        `df_map` é um dicionário onde as chaves são os nomes das tabelas na query SQL
        e os valores são os DataFrames Polars correspondentes.
        """
        sql_context = pl.SQLContext()
        for table_name, df in df_map.items():
            sql_context.register(table_name, df)
        return sql_context.execute(query).collect()

