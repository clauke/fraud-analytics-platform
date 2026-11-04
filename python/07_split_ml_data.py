from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# Fraud Analytics Platform
# Sprint 6 - Machine Learning
# Separacao dos dados para treinamento e validacao
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "fraud_ml_train.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

RANDOM_STATE = 42
TEST_SIZE = 0.20

def print_distribution(name, df):
    total = len(df)
    frauds = int(df["isFraud"].sum())
    fraud_rate = (frauds / total) * 100

    print(f"\n{name}")
    print(f"Total de registros: {total:,}")
    print(f"Fraudes: {frauds:,}")
    print(f"Transacoes legítimas: {total - frauds:,}")
    print(f"Taxa de fraude: {fraud_rate:.2f}%")

def main():

    print("=" * 60)
    print("Fraud Analytics Platform")
    print("Separacao dos dados para Machine Learning")
    print("=" * 60)

    # 1. Carregar dataset
    
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"\nDataset original: {len(df):,} registros")
    print(f"Colunas: {len(df.columns)}")

    # 2. Verificar colunas obrigatórias
    
    required_columns = [
        "TransactionID",
        "TransactionDT",
        "isFraud"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {missing_columns}"
        )

    # 3. Remover coluna auxiliar da análise temporal, 
    # caso esteja presente no CSV

    if "Periodo" in df.columns:
        df = df.drop(columns=["Periodo"])

    # 4. Verificar identificadores duplicados

    if df["TransactionID"].duplicated().any():
        raise ValueError(
            "Existem TransactionID duplicados no dataset."
        )

    # 5. Divisão estratificada

    train_stratified, validation_stratified = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df["isFraud"]
    )

    # 6. Divisão cronológica
    
    df_temporal = df.sort_values(
        "TransactionDT",
        ascending=True,
        kind="mergesort"
    ).reset_index(drop=True)

    split_index = int(len(df_temporal) * (1 - TEST_SIZE))

    train_chronological = df_temporal.iloc[:split_index].copy()
    validation_chronological = df_temporal.iloc[split_index:].copy()

    # 7. Criar diretório de saída

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 8. Exportar os arquivos

    files = {
        "fraud_train_stratified.csv": train_stratified,
        "fraud_validation_stratified.csv": validation_stratified,
        "fraud_train_chronological.csv": train_chronological,
        "fraud_validation_chronological.csv": validation_chronological,
    }

    for filename, dataset in files.items():
        output_path = OUTPUT_DIR / filename
        dataset.to_csv(output_path, index=False)
        print(f"\nArquivo gerado: {output_path.name}")

    # 9. Apresentar resultados

    print("\n" + "=" * 60)
    print("RESULTADOS DA DIVISAO")
    print("=" * 60)

    print_distribution(
        "Treinamento - Estratificado",
        train_stratified
    )

    print_distribution(
        "Validacao - Estratificada",
        validation_stratified
    )

    print_distribution(
        "Treinamento - Cronologico",
        train_chronological
    )

    print_distribution(
        "Validacao - Cronologica",
        validation_chronological
    )

    print("\nIntervalo temporal da divisao cronologica:")
    print(
        "Treinamento:",
        train_chronological["TransactionDT"].min(),
        "ate",
        train_chronological["TransactionDT"].max()
    )

    print(
        "Validacao:",
        validation_chronological["TransactionDT"].min(),
        "ate",
        validation_chronological["TransactionDT"].max()
    )

    print("\nProcesso concluido com sucesso.")


if __name__ == "__main__":
    main()