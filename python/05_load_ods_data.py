"""
===============================================================================
Fraud Analytics Platform
Carga STG -> ODS

Objetivo:
    Consolidar os dados das tabelas STG na camada ODS.

Origem:
    stg.train_transaction
    stg.test_transaction
    stg.train_identity
    stg.test_identity

Destino:
    ods.transactions
    ods.identities

===============================================================================
"""

import time
import uuid
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

SERVER = r"DESKTOP-R90TA06\SQL2022"
DATABASE = "FraudAnalytics"

SCHEMA_STG = "stg"
SCHEMA_ODS = "ods"

# =============================================================================
# CONEXÃO
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
# CONFIGURAÇÃO DAS CARGAS
# =============================================================================

TRANSACTION_SOURCES = [
    "train_transaction",
    "test_transaction",
]

IDENTITY_SOURCES = [
    "train_identity",
    "test_identity",
]

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def generate_batch_id():
    """Gera um identificador único para a execução da carga."""
    return str(uuid.uuid4())

def truncate_table(table_name):
    """Limpa a tabela ODS antes da carga."""

    sql = text(
        f"TRUNCATE TABLE {SCHEMA_ODS}.{table_name}"
    )

    with engine.begin() as conn:
        conn.execute(sql)

# =============================================================================
# CARGA TRANSACTIONS
# =============================================================================

def load_transactions(batch_id):
    """
    Consolida train_transaction e test_transaction em ods.transactions.
    """

    target_table = "transactions"

    print("-" * 70)
    print("STG -> ODS: transactions")

    start_time = time.time()

    truncate_table(target_table)

    total_rows = 0

    for source_table in TRANSACTION_SOURCES:

        print("-" * 70)
        print(f"Origem: {SCHEMA_STG}.{source_table}")

        query = f"""
            SELECT
                TransactionID,
                TransactionDT,
                TransactionAmt,
                ProductCD,
                card1,
                card2,
                card3,
                card4,
                card5,
                card6,
                addr1,
                addr2,
                dist1,
                dist2,
                P_emaildomain,
                R_emaildomain,
                DeviceType,
                DeviceInfo,
                isFraud
            FROM {SCHEMA_STG}.{source_table}
        """

        df = pd.read_sql(query, engine)
        rows = len(df)

        print(f"Registros: {rows:,}")

        if rows == 0:
            print("Nenhum registro encontrado.")
            continue

        # ---------------------------------------------------------------------
        # Metadados ETL
        # ---------------------------------------------------------------------

        df["source_file"] = f"{source_table}.csv"
        df["batch_id"] = batch_id
        df["etl_status"] = "LOADED"
        df["load_date"] = datetime.now().replace(microsecond=0)

        # ---------------------------------------------------------------------
        # Carga
        # ---------------------------------------------------------------------

        df.to_sql(
            name=target_table,
            con=engine,
            schema=SCHEMA_ODS,
            if_exists="append",
            index=False,
            chunksize=5000,
            method=None,
        )

        total_rows += rows

        print(
            f"Carga concluída: "
            f"{SCHEMA_ODS}.{target_table}"
        )

    elapsed = time.time() - start_time

    print("-" * 70)
    print(f"Total carregado: {total_rows:,}")
    print(f"Tempo: {elapsed:.2f} segundos")

    return total_rows, elapsed

# =============================================================================
# CARGA IDENTITIES
# =============================================================================

def load_identities(batch_id):
    """
    Consolida train_identity e test_identity
    em ods.identities.
    """

    target_table = "identities"

    print("-" * 70)
    print("STG -> ODS: identities")

    start_time = time.time()

    truncate_table(target_table)

    total_rows = 0

    for source_table in IDENTITY_SOURCES:

        print("-" * 70)
        print(f"Origem: {SCHEMA_STG}.{source_table}")

        query = f"""
            SELECT *
            FROM {SCHEMA_STG}.{source_table}
        """

        df = pd.read_sql(query, engine)

        rows = len(df)

        print(f"Registros: {rows:,}")

        if rows == 0:
            print("Nenhum registro encontrado.")
            continue

        # ---------------------------------------------------------------------
        # Selecionar somente as colunas existentes na tabela ODS
        # ---------------------------------------------------------------------

        ods_columns = [
            "TransactionID",

            "id_01",
            "id_02",
            "id_03",
            "id_04",
            "id_05",
            "id_06",
            "id_07",
            "id_08",
            "id_09",
            "id_10",

            "id_11",
            "id_12",
            "id_13",
            "id_14",
            "id_15",
            "id_16",
            "id_17",
            "id_18",
            "id_19",
            "id_20",

            "id_21",
            "id_22",
            "id_23",
            "id_24",
            "id_25",
            "id_26",
            "id_27",
            "id_28",
            "id_29",
            "id_30",

            "id_31",
            "id_32",
            "id_33",
            "id_34",
            "id_35",
            "id_36",
            "id_37",
            "id_38",

            "DeviceType",
            "DeviceInfo",
        ]

        existing_columns = [
            col for col in ods_columns
            if col in df.columns
        ]

        df = df[existing_columns]

        # ---------------------------------------------------------------------
        # Metadados ETL
        # ---------------------------------------------------------------------

        df["source_file"] = f"{source_table}.csv"
        df["batch_id"] = batch_id
        df["etl_status"] = "LOADED"
        df["load_date"] = datetime.now().replace(microsecond=0)

        # ---------------------------------------------------------------------
        # Carga
        # ---------------------------------------------------------------------

        df.to_sql(
            name=target_table,
            con=engine,
            schema=SCHEMA_ODS,
            if_exists="append",
            index=False,
            chunksize=5000,
            method=None,
        )

        total_rows += rows

        print(
            f"Carga concluída: "
            f"{SCHEMA_ODS}.{target_table}"
        )

    elapsed = time.time() - start_time

    print("-" * 70)
    print(f"Total carregado: {total_rows:,}")
    print(f"Tempo: {elapsed:.2f} segundos")

    return total_rows, elapsed

# =============================================================================
# MAIN
# =============================================================================

def main():
    batch_id = generate_batch_id()

    start_datetime = datetime.now()

    print("-" * 70)
    print("Fraud Analytics Platform")
    print("Carga STG -> ODS")
    print(start_datetime.strftime("%d/%m/%Y %H:%M:%S"))
    print(f"Batch ID: {batch_id}")
    print("-" * 70)

    try:

        # ---------------------------------------------------------------------
        # Transactions
        # ---------------------------------------------------------------------

        transaction_rows, transaction_time = load_transactions(
            batch_id
        )

        # ---------------------------------------------------------------------
        # Identities
        # ---------------------------------------------------------------------

        identity_rows, identity_time = load_identities(
            batch_id
        )

        # ---------------------------------------------------------------------
        # Resumo
        # ---------------------------------------------------------------------

        total_rows = transaction_rows + identity_rows
        total_time = transaction_time + identity_time

        print()
        print("=" * 70)
        print("CARGA STG -> ODS CONCLUÍDA")
        print("=" * 70)

        print(f"Batch ID:               {batch_id}")
        print(f"Transactions:           {transaction_rows:,}")
        print(f"Identities:             {identity_rows:,}")
        print(f"Total de registros:     {total_rows:,}")
        print(f"Tempo total:            {total_time:.2f} segundos")

        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("ERRO NA CARGA STG -> ODS")
        print("=" * 70)

        print(str(error))

        raise

# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()