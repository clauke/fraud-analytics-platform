"""
===============================================================================
Projeto: Fraud Analytics Platform
Arquivo: 04_load_stg_data.py
Objetivo: Carregar os dados da camada RAW para a camada STG
Banco: FraudAnalytics
===============================================================================
"""

from pathlib import Path
from datetime import datetime, timezone
import time
import uuid
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

SERVER = r"DESKTOP-R90TA06\SQL2022"
DATABASE = "FraudAnalytics"

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

BATCH_ID = uuid.uuid4()

# =============================================================================
# MAPEAMENTO RAW → STG
# =============================================================================

TABLES = {
    "train_transaction": {
        "source": "raw.train_transaction",
        "target": "stg.train_transaction",
        "file": "train_transaction.csv",
        "columns": [
            "TransactionID",
            "TransactionDT",
            "TransactionAmt",
            "ProductCD",
            "card1",
            "card2",
            "card3",
            "card4",
            "card5",
            "card6",
            "addr1",
            "addr2",
            "dist1",
            "dist2",
            "P_emaildomain",
            "R_emaildomain",
            "isFraud",
        ],
    },

    "train_identity": {
        "source": "raw.train_identity",
        "target": "stg.train_identity",
        "file": "train_identity.csv",
        "columns": [
            "TransactionID",
            "DeviceType",
            "DeviceInfo",
        ],
    },

    "test_transaction": {
        "source": "raw.test_transaction",
        "target": "stg.test_transaction",
        "file": "test_transaction.csv",
        "columns": [
            "TransactionID",
            "TransactionDT",
            "TransactionAmt",
            "ProductCD",
            "card1",
            "card2",
            "card3",
            "card4",
            "card5",
            "card6",
            "addr1",
            "addr2",
            "dist1",
            "dist2",
            "P_emaildomain",
            "R_emaildomain",
        ],
    },

    "test_identity": {
        "source": "raw.test_identity",
        "target": "stg.test_identity",
        "file": "test_identity.csv",
        "columns": [
            "TransactionID",
            "DeviceType",
            "DeviceInfo",
        ],
    },
}

# =============================================================================
# CARGA
# =============================================================================

def load_table(config):

    source = config["source"]
    target = config["target"]
    source_file = config["file"]
    columns = config["columns"]

    print("-" * 70)
    print(f"RAW → STG: {source}")

    start = time.time()

    query = f"SELECT {', '.join(columns)} FROM {source}"

    df = pd.read_sql(query, engine)

    df["source_file"] = source_file
    df["batch_id"] = BATCH_ID
    df["etl_status"] = "LOADED"
    df["load_date"] = datetime.now().replace(microsecond=0)

    rows = len(df)

    print(f"Registros: {rows:,}")

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {target}"))

    table_name = target.split(".")[1]

    df.to_sql(
        name=table_name,
        con=engine,
        schema="stg",
        if_exists="append",
        index=False,
        chunksize=5000,
        method=None,
    )

    elapsed = time.time() - start

    print(f"Carga concluída: {target}")
    print(f"Tempo: {elapsed:.2f} segundos")

    return rows, elapsed

# =============================================================================
# EXECUÇÃO
# =============================================================================

def main():

    print("=" * 70)
    print("Fraud Analytics Platform")
    print("Carga RAW → STG")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print(f"Batch ID: {BATCH_ID}")
    print("=" * 70)

    total_rows = 0
    total_time = 0

    for config in TABLES.values():
        rows, elapsed = load_table(config)
        total_rows += rows
        total_time += elapsed

    print()
    print("=" * 70)
    print("CARGA STG FINALIZADA")
    print("=" * 70)
    print(f"Registros processados: {total_rows:,}")
    print(f"Tempo total: {total_time:.2f} segundos")
    print("=" * 70)

if __name__ == "__main__":
    main()

