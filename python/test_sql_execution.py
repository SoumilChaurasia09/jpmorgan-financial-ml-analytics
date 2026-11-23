"""
Financial Performance & Profitability Analysis - SQL Verification & Test Runner
Executes schema.sql, loads processed CSVs into an in-memory SQLite database,
creates views from views.sql, and executes all 13 queries in data_analysis.sql.
"""

import os
import sqlite3
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(BASE_DIR, "sql")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

def test_sql():
    print("=" * 80)
    print("SQL SCRIPT VERIFICATION & EXECUTION TEST")
    print("=" * 80)
    
    conn = sqlite3.connect(":memory:")
    
    # 1. Execute schema.sql
    print("[*] Executing schema.sql...")
    with open(os.path.join(SQL_DIR, "schema.sql"), "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("  -> Schema DDL executed successfully.")
    
    # 2. Populate tables from CSVs
    table_files = {
        "dim_product": "dim_product.csv",
        "dim_country": "dim_country.csv",
        "dim_segment": "dim_segment.csv",
        "dim_date": "dim_date.csv",
        "fact_financials": "fact_financials.csv",
        "fact_budget": "simulated_budget.csv",
        "fact_operating_expenses": "simulated_operating_expenses.csv"
    }
    
    for table, file_name in table_files.items():
        file_path = os.path.join(DATA_DIR, file_name)
        df = pd.read_csv(file_path)
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"  -> Populated {table:<25} ({len(df):>4} rows)")
        
    # 3. Execute views.sql
    print("\n[*] Executing views.sql...")
    with open(os.path.join(SQL_DIR, "views.sql"), "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("  -> Views created successfully.")
    
    # 4. Parse queries in data_analysis.sql
    print("\n[*] Testing analytical queries in data_analysis.sql...")
    with open(os.path.join(SQL_DIR, "data_analysis.sql"), "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    # Regex split on headers like "-- QUERY 1: Title"
    blocks = re.findall(r"-- (QUERY \d+:[^\n]+)([\s\S]*?)(?=(?:-- QUERY \d+:|$))", raw_text)
    
    cur = conn.cursor()
    for q_title, q_body in blocks:
        # Split by semicolon inside block
        statements = [s.strip() for s in q_body.split(";") if s.strip()]
        for idx, stmt in enumerate(statements):
            # Remove comment-only lines
            lines = [l for l in stmt.split("\n") if not l.strip().startswith("--")]
            sql_clean = "\n".join(lines).strip()
            if not sql_clean:
                continue
                
            try:
                cur.execute(sql_clean)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                part_tag = f" (Part {idx+1})" if len(statements) > 1 else ""
                print(f"  [PASS] {q_title.strip()}{part_tag:<10} | Rows: {len(rows):<3} | Cols: {len(cols):<2}")
            except Exception as e:
                print(f"  [FAIL] {q_title.strip()}: {e}")
                print(f"SQL statement:\n{sql_clean}\n")
                raise e

    # 5. Validate Views
    views = [
        "vw_monthly_financial_summary",
        "vw_product_profitability",
        "vw_regional_performance",
        "vw_segment_performance",
        "vw_budget_vs_actual"
    ]
    print("\n[*] Validating analytical views output...")
    for v in views:
        cur.execute(f"SELECT COUNT(*) FROM {v}")
        cnt = cur.fetchone()[0]
        cur.execute(f"SELECT * FROM {v} LIMIT 1")
        cols = [d[0] for d in cur.description]
        print(f"  [PASS] View {v:<30} | Total Rows: {cnt:<4} | Total Columns: {len(cols)}")
        
    print("\n" + "=" * 80)
    print("ALL 13 SQL ANALYTICAL QUERIES & 5 VIEWS VERIFIED WITH ZERO ERRORS!")
    print("=" * 80)
    conn.close()

if __name__ == "__main__":
    test_sql()
