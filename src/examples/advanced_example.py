import polars as pl
import os

class AdvancedPolarsProcessor:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    def create_sample_data(self):
        # Criar dados de vendas simulados
        sales_data = {
            "order_id": range(1, 1001),
            "product": [f"Product_{i % 10}" for i in range(1000)],
            "category": [f"Category_{i % 3}" for i in range(1000)],
            "price": [round(10.0 + i % 50 + (i % 10) * 0.5, 2) for i in range(1000)],
            "quantity": [1 + i % 5 for i in range(1000)],
            "customer_id": [f"CUST_{i % 100}" for i in range(1000)],
            "order_date": pl.date_range(start=pl.date(2024, 1, 1), end=pl.date(2024, 10, 7), interval="1d", eager=True).sample(1000, with_replacement=True).sort().to_list()
        }
        sales_df = pl.DataFrame(sales_data)
        sales_df.write_csv(os.path.join(self.data_dir, "sales_data.csv"))
        print(f"Dados de vendas gerados e salvos em {os.path.join(self.data_dir, 'sales_data.csv')}")

        # Criar dados de clientes simulados
        customer_data = {
            "customer_id": [f"CUST_{i}" for i in range(100)],
            "region": [f"Region_{i % 4}" for i in range(100)],
            "loyalty_status": ["Gold" if i % 10 == 0 else "Silver" if i % 5 == 0 else "Bronze" for i in range(100)]
        }
        customer_df = pl.DataFrame(customer_data)
        customer_df.write_parquet(os.path.join(self.data_dir, "customer_data.parquet"))
        print(f"Dados de clientes gerados e salvos em {os.path.join(self.data_dir, 'customer_data.parquet')}")

        return sales_df, customer_df

    def load_data(self):
        sales_df = pl.read_csv(os.path.join(self.data_dir, "sales_data.csv"))
        customer_df = pl.read_parquet(os.path.join(self.data_dir, "customer_data.parquet"))
        return sales_df, customer_df

    def process_sales_data(self, sales_df: pl.DataFrame, customer_df: pl.DataFrame):
        # 1. Calcular o valor total da venda
        sales_df = sales_df.with_columns(
            (pl.col("price") * pl.col("quantity")).alias("total_sale_value")
        )

        # 2. Juntar com dados de clientes
        joined_df = sales_df.join(customer_df, on="customer_id", how="left")

        # 3. Análise de vendas por categoria e região
        sales_summary = joined_df.group_by(["category", "region"]).agg(
            pl.sum("total_sale_value").alias("total_revenue"),
            pl.count().alias("number_of_orders"),
            pl.mean("quantity").alias("avg_quantity_per_order")
        ).sort(pl.col("total_revenue"), descending=True)

        # 4. Clientes com maior gasto (Top 5)
        top_customers = joined_df.group_by("customer_id").agg(
            pl.sum("total_sale_value").alias("total_spent")
        ).sort(pl.col("total_spent"), descending=True).head(5)

        # 5. Vendas diárias (Lazy Evaluation)
        daily_sales_lazy = joined_df.lazy().with_columns(
            pl.col("order_date").cast(pl.Date).alias("day")
        ).group_by("day").agg(
            pl.sum("total_sale_value").alias("daily_revenue")
        ).sort("day")

        print("\n--- Resumo de Vendas por Categoria e Região ---")
        print(sales_summary)
        print("\n--- Top 5 Clientes por Gasto Total ---")
        print(top_customers)
        print("\n--- Vendas Diárias (Lazy Evaluation) ---")
        print(daily_sales_lazy.collect())

        return sales_summary, top_customers, daily_sales_lazy.collect()

if __name__ == "__main__":
    processor = AdvancedPolarsProcessor()
    sales_df, customer_df = processor.create_sample_data()
    processor.process_sales_data(sales_df, customer_df)

    print("\n==================================================")
    print("Demonstração Avançada Concluída.")
    print("==================================================")

