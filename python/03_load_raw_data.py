"""
===============================================================================
Projeto: Fraud Analytics Platform
Arquivo: 03_load_raw_data.py
Objetivo: Carregar os arquivos CSV para a camada RAW do SQL Server
Banco: FraudAnalytics
Schema: raw
===============================================================================
"""

from pathlib import Path
from datetime import datetime
import time

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# =============================================================================
# 1. CONFIGURAÇÕES
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

SERVER = r"DESKTOP-R90TA06\SQL2022"
DATABASE = "FraudAnalytics"
SCHEMA = "raw"

FILES = {
    "train_transaction.csv": "train_transaction",
    "train_identity.csv": "train_identity",
    "test_transaction.csv": "test_transaction",
    "test_identity.csv": "test_identity",
    "sample_submission.csv": "sample_submission",
}


# =============================================================================
# 2. CONEXÃO
# =============================================================================

connection_url = URL.create(
    "mssql+pyodbc",
    host=SERVER,
    database=DATABASE,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "trusted_connection": "yes",
    },
)

engine = create_engine(
    connection_url,
    fast_executemany=True,
)


# =============================================================================
# 3. CARGA DE UMA TABELA
# =============================================================================

def load_table(csv_file, table_name):

    csv_path = RAW_DIR / csv_file

    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    print("-" * 70)
    print(f"Carregando: {csv_file}")

    start = time.time()

    df = pd.read_csv(csv_path, low_memory=False)

    rows = len(df)

    print(f"Registros: {rows:,}")

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {SCHEMA}.{table_name}"))

    df.to_sql(
        name=table_name,
        con=engine,
        schema=SCHEMA,
        if_exists="append",
        index=False,
        chunksize=5000,
        method=None,
    )

    elapsed = time.time() - start

    print(f"Carga concluída: {table_name}")
    print(f"Tempo: {elapsed:.2f} segundos")

    return rows, elapsed


# =============================================================================
# 4. EXECUÇÃO
# =============================================================================

def main():

    print("=" * 70)
    print("Fraud Analytics Platform")
    print("Carga da camada RAW")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("=" * 70)

    total_rows = 0
    total_time = 0

    for csv_file, table_name in FILES.items():

        rows, elapsed = load_table(csv_file, table_name)

        total_rows += rows
        total_time += elapsed

    print()
    print("=" * 70)
    print("CARGA FINALIZADA")
    print("=" * 70)
    print(f"Registros carregados: {total_rows:,}")
    print(f"Tempo total: {total_time:.2f} segundos")
    print("=" * 70)


# =============================================================================
# 5. EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()