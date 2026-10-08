"""
===============================================================================
Fraud Analytics Platform
Carga STG -> ODS
Versão: 0.2

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

SCHEMA_RAW = "raw"
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

        if source_table == "train_transaction":

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
                    isFraud
                FROM {SCHEMA_STG}.{source_table}
            """

        else:

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
                    CAST(NULL AS bit) AS isFraud
                FROM {SCHEMA_STG}.{source_table}
            """

        df = pd.read_sql(query, engine)
        rows = len(df)

        print(f"Registros: {rows:,}")

        if rows == 0:
            print("Nenhum registro encontrado.")
            continue

        # ---------------------------------------------------------------------
        # Data source
        # --------------------------------------------------------------------- 
        
        if source_table == "train_transaction": 
            df["data_source"] = "train" 
        else: df["data_source"] = "test"

        # ---------------------------------------------------------------------
        # Metadados ETL
        # ---------------------------------------------------------------------

        df["source_file"] = f"{source_table}.csv"
        df["batch_id"] = batch_id
        df["load_date"] = datetime.now().replace(microsecond=0)
        df["etl_status"] = "LOADED"

        # --------------------------------------------------------------------- 
        # Ordem das colunas da ODS 
        # ---------------------------------------------------------------------

        ods_columns = [
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

            "data_source",
            "source_file",
            "batch_id",
            "load_date",
            "etl_status",
        ]

        df = df[ods_columns]

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
    Consolida train_identity e test_identity em ods.identities.

    Estratégia:
        - id_01 a id_38: origem RAW
        - DeviceType e DeviceInfo: origem STG
        - Chave de integração: TransactionID
    """

    target_table = "identities"

    print("-" * 70)
    print("RAW + STG -> ODS: identities")

    start_time = time.time()

    truncate_table(target_table)

    total_rows = 0

    for source_table in IDENTITY_SOURCES:

        print("-" * 70)
        print(f"RAW: {SCHEMA_RAW}.{source_table}")
        print(f"STG: {SCHEMA_STG}.{source_table}")

        if source_table == "train_identity":

            query = f"""
                SELECT
                    r.TransactionID,

                    r.id_01,
                    r.id_02,
                    r.id_03,
                    r.id_04,
                    r.id_05,
                    r.id_06,
                    r.id_07,
                    r.id_08,
                    r.id_09,
                    r.id_10,
                    r.id_11,
                    r.id_12,
                    r.id_13,
                    r.id_14,
                    r.id_15,
                    r.id_16,
                    r.id_17,
                    r.id_18,
                    r.id_19,
                    r.id_20,
                    r.id_21,
                    r.id_22,
                    r.id_23,
                    r.id_24,
                    r.id_25,
                    r.id_26,
                    r.id_27,
                    r.id_28,
                    r.id_29,
                    r.id_30,
                    r.id_31,
                    r.id_32,
                    r.id_33,
                    r.id_34,
                    r.id_35,
                    r.id_36,
                    r.id_37,
                    r.id_38,
                    s.DeviceType,
                    s.DeviceInfo

                FROM {SCHEMA_RAW}.{source_table} r
                LEFT JOIN {SCHEMA_STG}.{source_table} s
                    ON r.TransactionID = s.TransactionID
            """

        else:

            query = f"""
                SELECT
                    r.TransactionID,
                    r.[id-01] AS id_01,
                    r.[id-02] AS id_02,
                    r.[id-03] AS id_03,
                    r.[id-04] AS id_04,
                    r.[id-05] AS id_05,
                    r.[id-06] AS id_06,
                    r.[id-07] AS id_07,
                    r.[id-08] AS id_08,
                    r.[id-09] AS id_09,
                    r.[id-10] AS id_10,
                    r.[id-11] AS id_11,
                    r.[id-12] AS id_12,
                    r.[id-13] AS id_13,
                    r.[id-14] AS id_14,
                    r.[id-15] AS id_15,
                    r.[id-16] AS id_16,
                    r.[id-17] AS id_17,
                    r.[id-18] AS id_18,
                    r.[id-19] AS id_19,
                    r.[id-20] AS id_20,
                    r.[id-21] AS id_21,
                    r.[id-22] AS id_22,
                    r.[id-23] AS id_23,
                    r.[id-24] AS id_24,
                    r.[id-25] AS id_25,
                    r.[id-26] AS id_26,
                    r.[id-27] AS id_27,
                    r.[id-28] AS id_28,
                    r.[id-29] AS id_29,
                    r.[id-30] AS id_30,
                    r.[id-31] AS id_31,
                    r.[id-32] AS id_32,
                    r.[id-33] AS id_33,
                    r.[id-34] AS id_34,
                    r.[id-35] AS id_35,
                    r.[id-36] AS id_36,
                    r.[id-37] AS id_37,
                    r.[id-38] AS id_38,
                    s.DeviceType,
                    s.DeviceInfo
                FROM {SCHEMA_RAW}.{source_table} r
                LEFT JOIN {SCHEMA_STG}.{source_table} s
                    ON r.TransactionID = s.TransactionID
            """

        df = pd.read_sql(query, engine)

        rows = len(df)

        print(f"Registros: {rows:,}")

        if rows == 0:
            print("Nenhum registro encontrado.")
            continue

        # --------------------------------------------------------------------- 
        # Data source 
        # --------------------------------------------------------------------- 
        
        if source_table == "train_identity": 
            df["data_source"] = "train" 
        else: df["data_source"] = "test"

        # ---------------------------------------------------------------------
        # Metadados ETL
        # ---------------------------------------------------------------------

        df["source_file"] = f"{source_table}.csv"
        df["batch_id"] = batch_id
        df["etl_status"] = "LOADED"
        df["load_date"] = datetime.now().replace(microsecond=0)

        # ---------------------------------------------------------------------
        # Ordem das colunas da ODS
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

            "data_source",
            "source_file",
            "batch_id",
            "load_date",
            "etl_status",
        ]

        df = df[ods_columns]

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