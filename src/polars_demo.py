"""
Polars High-Speed DataFrames
Author: Gabriel Demetrios Lafis
Year: 2025
"""

import polars as pl
import time

def polars_performance_demo():
    """Demonstra performance do Polars"""
    
    # Criar DataFrame grande
    print("Creating large dataset...")
    df = pl.DataFrame({
        "id": range(1000000),
        "value": [i * 2.5 for i in range(1000000)],
        "category": [f"CAT{i % 10}" for i in range(1000000)]
    })
    
    # Operações em cadeia (lazy evaluation)
    start = time.time()
    result = (
        df.lazy()
        .filter(pl.col("value") > 1000)
        .group_by("category")
        .agg([
            pl.col("value").mean().alias("avg_value"),
            pl.col("value").sum().alias("total_value"),
            pl.count().alias("count")
        ])
        .sort("total_value", descending=True)
        .collect()
    )
    elapsed = time.time() - start
    
    print(f"\n✓ Processed 1M rows in {elapsed:.3f}s")
    print("\nTop Categories:")
    print(result.head())

if __name__ == "__main__":
    print("=" * 60)
    print("Polars High-Speed DataFrames Demo")
    print("=" * 60)
    polars_performance_demo()
