"""
Fraud Analytics Platform
Sprint 6 - Preparação dos dados para Machine Learning

Extrai as transações rotuladas da camada ODS,
complementando-as com os atributos de identidade.
"""

from pathlib import Path
import pandas as pd
import pyodbc

# ============================================================
# 1. CONFIGURAÇÕES
# ============================================================

SERVER = r"DESKTOP-R90TA06\SQL2022"
DATABASE = "FraudAnalytics"

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "fraud_ml_train.csv"

# ============================================================
# 2. CONSULTA SQL
# ============================================================

QUERY = """
SELECT
    t.TransactionID,
    t.TransactionDT,
    t.TransactionAmt,
    t.ProductCD,
    t.card1,
    t.card2,
    t.card3,
    t.card4,
    t.card5,
    t.card6,
    t.addr1,
    t.addr2,
    t.dist1,
    t.dist2,
    t.P_emaildomain,
    t.R_emaildomain,
    t.isFraud,

    i.id_01,
    i.id_02,
    i.id_03,
    i.id_04,
    i.id_05,
    i.id_06,
    i.id_07,
    i.id_08,
    i.id_09,
    i.id_10,
    i.id_11,
    i.id_12,
    i.id_13,
    i.id_14,
    i.id_15,
    i.id_16,
    i.id_17,
    i.id_18,
    i.id_19,
    i.id_20,
    i.id_21,
    i.id_22,
    i.id_23,
    i.id_24,
    i.id_25,
    i.id_26,
    i.id_27,
    i.id_28,
    i.id_29,
    i.id_30,
    i.id_31,
    i.id_32,
    i.id_33,
    i.id_34,
    i.id_35,
    i.id_36,
    i.id_37,
    i.id_38,
    i.DeviceType,
    i.DeviceInfo

FROM ods.transactions AS t

LEFT JOIN ods.identities AS i
    ON t.TransactionID = i.TransactionID
    AND t.data_source = i.data_source

WHERE t.data_source = 'train';
"""

# ============================================================
# 3. EXTRAÇÃO E EXPORTAÇÃO
# ============================================================

def main():

    print("=" * 60)
    print("FRAUD ANALYTICS PLATFORM")
    print("Preparação dos dados para Machine Learning")
    print("=" * 60)

    print("\nConectantdo ao SQL Server...")

    with pyodbc.connect(CONNECTION_STRING) as connection:

        print("Conexão estabelecida.")
        print("\nExtraindo transações de treinamento...")

        df = pd.read_sql_query(QUERY, connection)

    print("\nExtração concluída.")

    # --------------------------------------------------------
    # 4. VERIFICAÇÕES INICIAIS
    # --------------------------------------------------------

    print("\nResumo dos dados:")

    print(f"Total de registros: {len(df):,}")
    print(f"Total de colunas: {len(df.columns)}")

    print("\nDistribuição da variável-alvo:")

    print(
        df["isFraud"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nPercentual de cada classe:")

    print(
        (df["isFraud"].value_counts(normalize=True) * 100)
        .sort_index()
        .round(2)
        .to_string()
    )

    print("\nValores ausentes:")

    print(
        f"Total de células nulas: "
        f"{df.isna().sum().sum():,}"
    )

    print("\nTransações duplicadas:")

    print(
        f"TransactionID duplicados: "
        f"{df['TransactionID'].duplicated().sum():,}"
    )

    print("\nDistribuição temporal das transações:")

    print(f"TransactionDT mínimo: {df['TransactionDT'].min()}")
    print(f"TransactionDT máximo: {df['TransactionDT'].max()}")

    print("\nFraudes por período temporal:")

    df["Periodo"] = pd.qcut(
        df["TransactionDT"],
        q=6,
        labels=False
    )

    resumo_temporal = df.groupby("Periodo", observed=True).agg(
        TotalTransacoes=("TransactionID", "count"),
        TotalFraudes=("isFraud", "sum")
    )

    resumo_temporal["PercentualFraude"] = (
        resumo_temporal["TotalFraudes"]
        / resumo_temporal["TotalTransacoes"] * 100
    ).round(2)

    print(resumo_temporal)

    # --------------------------------------------------------
    # 5. EXPORTAÇÃO
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\nArquivo exportado com sucesso!")
    print(f"Local: {OUTPUT_FILE}")

    print("\nProcesso finalizado.")

if __name__ == "__main__":
    main()