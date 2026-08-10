
"""
===============================================================================
Projeto: Fraud Analytics Platform
Arquivo: generate_raw_ddl.py
Objetivo: Gerar automaticamente o DDL das tabelas da camada RAW
Fonte: IEEE-CIS Fraud Detection Dataset
===============================================================================
"""

from pathlib import Path
import pandas as pd


# =============================================================================
# 1. CONFIGURAÇÕES
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
SQL_DIR = PROJECT_ROOT / "sql"

OUTPUT_FILE = SQL_DIR / "02_create_raw_tables.sql"


FILES = {
    "train_transaction.csv": "train_transaction",
    "train_identity.csv": "train_identity",
    "test_transaction.csv": "test_transaction",
    "test_identity.csv": "test_identity",
    "sample_submission.csv": "sample_submission",
}


# =============================================================================
# 2. MAPEAMENTO DE TIPOS
# =============================================================================

def map_dtype(dtype):
    """
    Converte tipos do Pandas para tipos compatíveis com SQL Server.
    """

    if pd.api.types.is_bool_dtype(dtype):
        return "BIT"

    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"

    if pd.api.types.is_float_dtype(dtype):
        return "DECIMAL(18,4)"

    return "VARCHAR(255)"


# =============================================================================
# 3. GERAÇÃO DO DDL DE UMA TABELA
# =============================================================================

def generate_table_ddl(csv_file, table_name):
    """
    Gera o CREATE TABLE correspondente a um arquivo CSV.
    """

    csv_path = RAW_DIR / csv_file

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {csv_path}"
        )

    print(f"Lendo metadata: {csv_file}")

    # Apenas o cabeçalho e algumas linhas são suficientes
    # para inferência inicial dos tipos.
    df = pd.read_csv(
        csv_path,
        nrows=1000,
        low_memory=False
    )

    columns = []

    for column in df.columns:

        dtype = map_dtype(df[column].dtype)

        # Proteção contra nomes inválidos no SQL Server
        column_name = column.replace("]", "]]")

        columns.append(
            f"        [{column_name}] {dtype} NULL"
        )

    columns_sql = ",\\n".join(columns)

    ddl = f"""
/* ============================================================================
   Tabela: raw.{table_name}
   Origem: {csv_file}
   ============================================================================ */

IF OBJECT_ID('raw.{table_name}', 'U') IS NULL
BEGIN

    CREATE TABLE raw.{table_name}
    (
{columns_sql}
    );

END;
GO

"""

    return ddl

# =============================================================================
# 4. GERAÇÃO DO ARQUIVO SQL
# =============================================================================

def main():

    SQL_DIR.mkdir(parents=True, exist_ok=True)

    sql_content = """/*
===============================================================================
Projeto: Fraud Analytics Platform
Arquivo: 02_create_raw_tables.sql
Objetivo: Criação das tabelas da camada RAW
Banco: FraudAnalytics
Schema: raw
Versão: 0.1
===============================================================================
*/

USE FraudAnalytics;
GO

"""

    for csv_file, table_name in FILES.items():

        ddl = generate_table_ddl(
            csv_file,
            table_name
        )

        sql_content += ddl

    sql_content += """
/* ============================================================================
   FIM DO SCRIPT
   ============================================================================ */
"""

    OUTPUT_FILE.write_text(
        sql_content,
        encoding="utf-8"
    )

    print()
    print("DDL gerado com sucesso!")
    print(f"Arquivo: {OUTPUT_FILE}")


# =============================================================================
# 5. EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()

