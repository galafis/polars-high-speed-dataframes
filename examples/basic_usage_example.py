"""
Basic Usage Examples for Polars High-Speed DataFrames
Author: Gabriel Demetrios Lafis
Year: 2025

This module provides simple, practical examples of using Polars for data processing.
"""

import polars as pl
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.polars_demo import PolarsDataProcessor


def example_1_basic_dataframe():
    """Example 1: Creating and displaying a basic DataFrame."""
    print("\n" + "="*60)
    print("Example 1: Basic DataFrame Creation")
    print("="*60)
    
    data = {
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "age": [25, 30, 35, 28],
        "city": ["New York", "London", "Paris", "Tokyo"],
        "salary": [50000, 70000, 60000, 55000]
    }
    
    df = pl.DataFrame(data)
    print("\nOriginal DataFrame:")
    print(df)
    
    print("\nDataFrame Info:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns}")
    print(f"Data Types: {df.dtypes}")


def example_2_filtering_and_selection():
    """Example 2: Filtering and selecting data."""
    print("\n" + "="*60)
    print("Example 2: Filtering and Selection")
    print("="*60)
    
    processor = PolarsDataProcessor()
    
    data = {
        "product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headset"],
        "price": [1200, 25, 75, 300, 80],
        "stock": [15, 100, 50, 30, 45],
        "category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories"]
    }
    
    df = processor.load_data_from_dict(data)
    print("\nOriginal Data:")
    print(df)
    
    # Filter products over $100
    expensive_products = processor.filter_by_condition(df, pl.col("price") > 100)
    print("\nProducts over $100:")
    print(expensive_products)
    
    # Select specific columns
    print("\nProduct names and prices:")
    print(df.select(["product", "price"]))


def example_3_aggregations():
    """Example 3: Grouping and aggregations."""
    print("\n" + "="*60)
    print("Example 3: Grouping and Aggregations")
    print("="*60)
    
    processor = PolarsDataProcessor()
    
    data = {
        "first_name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "last_name": ["Smith", "Jones", "Brown", "Wilson", "Davis"],
        "age": [25, 30, 35, 28, 40],
        "department": ["Sales", "Engineering", "Sales", "HR", "Engineering"],
        "monthly_salary": [50000, 70000, 60000, 55000, 80000]
    }
    
    df = processor.load_data_from_dict(data)
    print("\nEmployee Data:")
    print(df)
    
    # Calculate statistics by department
    stats = processor.calculate_summary_statistics(df, "department", "monthly_salary")
    print("\nSalary Statistics by Department:")
    print(stats)


def example_4_transformations():
    """Example 4: Data transformations and new columns."""
    print("\n" + "="*60)
    print("Example 4: Data Transformations")
    print("="*60)
    
    processor = PolarsDataProcessor()
    
    data = {
        "first_name": ["Alice", "Bob", "Charlie"],
        "last_name": ["Smith", "Jones", "Brown"],
        "age": [25, 30, 45],
        "city": ["New York", "London", "Paris"],
        "monthly_salary": [50000, 70000, 60000]
    }
    
    df = processor.load_data_from_dict(data)
    print("\nOriginal Data:")
    print(df)
    
    # Add derived columns
    df_transformed = processor.add_derived_columns(df)
    print("\nData with Derived Columns:")
    print(df_transformed)


def example_5_joins():
    """Example 5: Joining DataFrames."""
    print("\n" + "="*60)
    print("Example 5: Joining DataFrames")
    print("="*60)
    
    processor = PolarsDataProcessor()
    
    employees = {
        "employee_id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "department_id": [10, 20, 10, 30]
    }
    
    departments = {
        "department_id": [10, 20, 30],
        "department_name": ["Sales", "Engineering", "HR"],
        "location": ["New York", "San Francisco", "Chicago"]
    }
    
    df_employees = processor.load_data_from_dict(employees)
    df_departments = processor.load_data_from_dict(departments)
    
    print("\nEmployees:")
    print(df_employees)
    print("\nDepartments:")
    print(df_departments)
    
    # Perform join
    joined = processor.perform_join(df_employees, df_departments, "department_id", how="inner")
    print("\nJoined Data:")
    print(joined)


def example_6_file_operations():
    """Example 6: Reading and writing files."""
    print("\n" + "="*60)
    print("Example 6: File Operations (CSV and Parquet)")
    print("="*60)
    
    processor = PolarsDataProcessor()
    
    data = {
        "id": [1, 2, 3, 4, 5],
        "product": ["Apple", "Banana", "Orange", "Grape", "Mango"],
        "quantity": [100, 150, 80, 200, 120],
        "price": [0.5, 0.3, 0.6, 2.5, 1.2]
    }
    
    df = processor.load_data_from_dict(data)
    
    # Create temp directory for examples
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    # Write to CSV
    csv_path = os.path.join(temp_dir, "products.csv")
    processor.write_csv(df, csv_path)
    print(f"\nData written to CSV: {csv_path}")
    
    # Read from CSV
    df_from_csv = processor.read_csv(csv_path)
    print("\nData read from CSV:")
    print(df_from_csv)
    
    # Write to Parquet
    parquet_path = os.path.join(temp_dir, "products.parquet")
    processor.write_parquet(df, parquet_path)
    print(f"\nData written to Parquet: {parquet_path}")
    
    # Read from Parquet
    df_from_parquet = processor.read_parquet(parquet_path)
    print("\nData read from Parquet:")
    print(df_from_parquet)
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    print(f"\nTemporary files cleaned up.")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("POLARS HIGH-SPEED DATAFRAMES - BASIC USAGE EXAMPLES")
    print("="*60)
    
    example_1_basic_dataframe()
    example_2_filtering_and_selection()
    example_3_aggregations()
    example_4_transformations()
    example_5_joins()
    example_6_file_operations()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
