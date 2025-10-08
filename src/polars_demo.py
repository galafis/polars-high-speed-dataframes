
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
            pl.count().alias("count")
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
            (pl.col("monthly_salary") * 12).alias("annual_salary").fill_null(0) # Exemplo de tratamento de nulos
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
        return sql_context.execute(query).fetch()


if __name__ == "__main__":
    print("=" * 60)
    print("Polars High-Speed DataFrames Advanced Demo")
    print("=" * 60)

    processor = PolarsDataProcessor()
    data_dir = "./polars_data"
    os.makedirs(data_dir, exist_ok=True)

    # 1. Carregar dados de um dicionário
    print("\n--- 1. Carregando dados de dicionário ---")
    employee_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "first_name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"],
        "last_name": ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"],
        "age": [24, 27, 32, 45, 29, 58, 35, 40, 21, 50],
        "city": ["NY", "LA", "NY", "SF", "LA", "NY", "SF", "LA", "NY", "SF"],
        "monthly_salary": [5000, 6000, 4500, 7500, 6200, 8000, 5500, 9000, 4000, 7000],
        "department": ["HR", "IT", "HR", "IT", "Finance", "HR", "IT", "Finance", "HR", "IT"]
    }
    df_employees = processor.load_data_from_dict(employee_data)
    print("DataFrame de Funcionários Original:")
    print(df_employees)

    # 2. Adicionar colunas derivadas
    print("\n--- 2. Adicionando colunas derivadas ---")
    df_employees_derived = processor.add_derived_columns(df_employees)
    print("DataFrame com Colunas Derivadas:")
    print(df_employees_derived)

    # 3. Filtrar por condição
    print("\n--- 3. Filtrando por condição (idade > 30 e salário anual > 60000) ---")
    filtered_df = processor.filter_by_condition(
        df_employees_derived,
        (pl.col("age") > 30) & (pl.col("annual_salary") > 60000)
    )
    print("DataFrame Filtrado:")
    print(filtered_df)

    # 4. Calcular estatísticas de resumo
    print("\n--- 4. Estatísticas de resumo por Departamento ---")
    summary_stats = processor.calculate_summary_statistics(df_employees_derived, "department", "annual_salary")
    print("Estatísticas de Salário Anual por Departamento:")
    print(summary_stats)

    # 5. Aplicar função de janela
    print("\n--- 5. Aplicando função de janela (Rolling Mean e Rank por Departamento) ---")
    df_window = processor.apply_window_function(df_employees_derived, "department", "annual_salary", "annual_salary")
    print("DataFrame com Funções de Janela:")
    print(df_window)

    # 6. Simular dados com valores nulos e tratar
    print("\n--- 6. Tratamento de Dados Ausentes ---")
    data_with_nulls = {
        "id": [1, 2, 3, 4],
        "value": [10, None, 30, 40],
        "category": ["A", "B", "A", "C"]
    }
    df_nulls = processor.load_data_from_dict(data_with_nulls)
    print("DataFrame com Nulos Original:")
    print(df_nulls)

    print("Preenchendo nulos com a média:")
    df_filled_mean = processor.handle_missing_data(df_nulls, strategy="mean", column="value")
    print(df_filled_mean)

    print("Preenchendo nulos com forward fill:")
    df_filled_ffill = processor.handle_missing_data(df_nulls, strategy="forward_fill", column="value")
    print(df_filled_ffill)

    # 7. Leitura e Escrita de Arquivos (CSV e Parquet)
    print("\n--- 7. Leitura e Escrita de Arquivos (CSV e Parquet) ---")
    csv_file = os.path.join(data_dir, "employees.csv")
    parquet_file = os.path.join(data_dir, "employees.parquet")

    processor.write_csv(df_employees_derived, csv_file)
    df_from_csv = processor.read_csv(csv_file)
    print("DataFrame lido de CSV:")
    print(df_from_csv.head(2))

    processor.write_parquet(df_employees_derived, parquet_file)
    df_from_parquet = processor.read_parquet(parquet_file)
    print("DataFrame lido de Parquet:")
    print(df_from_parquet.head(2))

    # 8. Executar query SQL em DataFrames Polars
    print("\n--- 8. Executando Query SQL em DataFrames Polars ---")
    department_info = {
        "department": ["HR", "IT", "Finance"],
        "head_count": [3, 4, 2],
        "budget": [150000, 200000, 100000]
    }
    df_departments = processor.load_data_from_dict(department_info)

    sql_query = """
        SELECT
            e.full_name,
            e.age_group,
            e.annual_salary,
            d.budget
        FROM employees AS e
        JOIN departments AS d
        ON e.department = d.department
        WHERE e.age < 40
        ORDER BY e.annual_salary DESC
    """
    df_sql_result = processor.execute_sql_query(
        {"employees": df_employees_derived, "departments": df_departments},
        sql_query
    )
    print("Resultado da Query SQL:")
    print(df_sql_result)

    # Limpeza
    os.remove(csv_file)
    os.remove(parquet_file)
    os.rmdir(data_dir)

    print("=" * 60)
    print("Exemplo Concluído")
    print("=" * 60)

