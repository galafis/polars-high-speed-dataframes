#!/usr/bin/env python3
"""
Polars High-Speed DataFrames - Complete Demo
Author: Gabriel Demetrios Lafis
Year: 2025

This script runs a complete demonstration of all repository features.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.polars_demo import PolarsDataProcessor
from examples.advanced_example import AdvancedPolarsProcessor
import polars as pl


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_basic_operations():
    """Demonstrate basic Polars operations."""
    print_header("1. BASIC OPERATIONS DEMO")
    
    processor = PolarsDataProcessor()
    
    # Create sample data
    data = {
        "first_name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "last_name": ["Smith", "Jones", "Brown", "Wilson", "Davis"],
        "age": [25, 30, 35, 28, 40],
        "city": ["New York", "London", "New York", "Paris", "London"],
        "monthly_salary": [50000, 70000, 60000, 55000, 80000]
    }
    
    df = processor.load_data_from_dict(data)
    print("\n✓ DataFrame created successfully")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {df.columns}")
    
    # Add derived columns
    df_enhanced = processor.add_derived_columns(df)
    print("\n✓ Derived columns added (full_name, age_group, annual_salary)")
    print(f"  New columns: {[c for c in df_enhanced.columns if c not in df.columns]}")
    
    # Calculate statistics
    stats = processor.calculate_summary_statistics(df, "city", "monthly_salary")
    print("\n✓ Statistics calculated by city")
    print(stats)
    
    return df


def demo_file_operations():
    """Demonstrate file I/O operations."""
    print_header("2. FILE I/O OPERATIONS DEMO")
    
    processor = PolarsDataProcessor()
    
    # Create test data
    data = {
        "product_id": list(range(1, 11)),
        "product_name": [f"Product_{i}" for i in range(1, 11)],
        "price": [10.0 + i * 5.5 for i in range(10)],
        "quantity": [100 - i * 5 for i in range(10)]
    }
    df = processor.load_data_from_dict(data)
    
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Write CSV
        csv_path = os.path.join(temp_dir, "products.csv")
        processor.write_csv(df, csv_path)
        
        # Read CSV
        df_csv = processor.read_csv(csv_path)
        print(f"\n✓ CSV operations successful")
        print(f"  Rows written/read: {df_csv.shape[0]}")
        
        # Write Parquet
        parquet_path = os.path.join(temp_dir, "products.parquet")
        processor.write_parquet(df, parquet_path)
        
        # Read Parquet
        df_parquet = processor.read_parquet(parquet_path)
        print(f"\n✓ Parquet operations successful")
        print(f"  Rows written/read: {df_parquet.shape[0]}")
        
    finally:
        shutil.rmtree(temp_dir)
        print("\n✓ Temporary files cleaned up")


def demo_advanced_processing():
    """Demonstrate advanced processing with real-world scenario."""
    print_header("3. ADVANCED PROCESSING DEMO")
    
    processor = AdvancedPolarsProcessor()
    
    # Override data directory to use temp
    import tempfile
    import shutil
    temp_dir = tempfile.mkdtemp()
    processor.data_dir = temp_dir
    
    try:
        print("\n✓ Generating sample sales and customer data...")
        sales_df, customer_df = processor.create_sample_data()
        print(f"  Sales records: {sales_df.shape[0]}")
        print(f"  Customer records: {customer_df.shape[0]}")
        
        print("\n✓ Processing sales data with joins and aggregations...")
        sales_summary, top_customers, daily_sales = processor.process_sales_data(
            sales_df, customer_df
        )
        
        print(f"\n✓ Sales analysis complete:")
        print(f"  Category-Region combinations: {sales_summary.shape[0]}")
        print(f"  Top customers identified: {top_customers.shape[0]}")
        print(f"  Daily sales records: {daily_sales.shape[0]}")
        
        print("\n  Top 3 customers by spending:")
        print(top_customers.head(3).select(["customer_id", "total_spent"]))
        
    finally:
        shutil.rmtree(temp_dir)


def demo_data_transformations():
    """Demonstrate various data transformations."""
    print_header("4. DATA TRANSFORMATIONS DEMO")
    
    processor = PolarsDataProcessor()
    
    # Create sample data
    data = {
        "product": ["A", "B", "C", "D", "E", "A", "B", "C"],
        "category": ["X", "Y", "X", "Y", "X", "X", "Y", "X"],
        "sales": [100, 150, 200, 175, 125, 110, 160, 210],
        "date": ["2024-01-01"] * 8
    }
    df = processor.load_data_from_dict(data)
    
    # Filtering
    filtered = processor.filter_by_condition(df, pl.col("sales") > 150)
    print(f"\n✓ Filtered data (sales > 150): {filtered.shape[0]} rows")
    
    # Joining
    other_data = {
        "product": ["A", "B", "C"],
        "supplier": ["Supplier1", "Supplier2", "Supplier1"]
    }
    other_df = processor.load_data_from_dict(other_data)
    joined = processor.perform_join(df, other_df, "product", how="inner")
    print(f"✓ Joined with supplier data: {joined.shape[0]} rows")
    
    # SQL Query
    df_map = {"sales": df}
    result = processor.execute_sql_query(
        df_map, 
        "SELECT category, SUM(sales) as total_sales FROM sales GROUP BY category ORDER BY total_sales DESC"
    )
    print("\n✓ SQL query executed:")
    print(result)


def run_tests():
    """Run the test suite."""
    print_header("5. RUNNING TEST SUITE")
    
    import subprocess
    
    print("\n✓ Executing pytest...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    # Print summary
    lines = result.stdout.split('\n')
    for line in lines:
        if 'passed' in line.lower() or 'failed' in line.lower() or 'error' in line.lower():
            print(f"  {line}")
    
    return result.returncode == 0


def main():
    """Run complete demonstration."""
    print("\n" + "=" * 70)
    print("  POLARS HIGH-SPEED DATAFRAMES - COMPLETE DEMONSTRATION")
    print("  Author: Gabriel Demetrios Lafis")
    print("  Year: 2025")
    print("=" * 70)
    
    try:
        # Run all demos
        demo_basic_operations()
        demo_file_operations()
        demo_advanced_processing()
        demo_data_transformations()
        
        # Run tests
        tests_passed = run_tests()
        
        # Final summary
        print_header("DEMONSTRATION COMPLETE")
        
        if tests_passed:
            print("\n✅ All demonstrations completed successfully!")
            print("✅ All tests passed!")
        else:
            print("\n⚠️  Demonstrations completed, but some tests failed.")
        
        print("\nRepository features validated:")
        print("  ✓ Basic DataFrame operations")
        print("  ✓ File I/O (CSV, Parquet)")
        print("  ✓ Advanced processing and aggregations")
        print("  ✓ Data transformations and SQL queries")
        print("  ✓ Comprehensive test suite")
        print("\n" + "=" * 70 + "\n")
        
        return 0 if tests_passed else 1
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
