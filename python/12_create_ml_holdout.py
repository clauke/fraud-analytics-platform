"""
Fraud Analytics Platform
Criação dos conjuntos de treinamento, validação e teste independente.

Divisões:
- Estratificada: 60% treinamento, 20% validação e 20% teste.
- Cronológica: 60% treinamento, 20% validação e 20% teste.

O conjunto de teste será reservado para a avaliação final dos modelos.
"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "fraud_ml_train.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

TARGET = "isFraud"
TIME_COLUMN = "TransactionDT"

RANDOM_STATE = 42

TRAIN_SIZE = 0.60
VALIDATION_SIZE = 0.20
TEST_SIZE = 0.20

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def display_dataset_info(name, dataframe):
    """Exibe informações básicas de cada conjunto."""

    total = len(dataframe)
    frauds = int(dataframe[TARGET].sum())
    fraud_rate = (frauds / total) * 100 if total > 0 else 0

    print(f"\n{name}")
    print("-" * 55)
    print(f"Registros: {total:,}")
    print(f"Fraudes: {frauds:,}")
    print(f"Não fraudes: {total - frauds:,}")
    print(f"Percentual de fraudes: {fraud_rate:.2f}%")

def save_dataset(dataframe, filename):
    """Salva o conjunto em formato CSV."""

    output_path = OUTPUT_DIR / filename
    dataframe.to_csv(output_path, index=False)

    print(f"Arquivo salvo: {output_path}")

# ============================================================
# CARREGAMENTO DA BASE
# ============================================================

def main():

    print("=" * 65)
    print("Fraud Analytics Platform")
    print("Criação dos conjuntos de ML - Holdout")
    print("=" * 65)

    print("\nCarregando base original...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Registros carregados: {len(df):,}")
    print(f"Quantidade de colunas: {len(df.columns)}")

    # Verificação das colunas necessárias
    required_columns = [TARGET, TIME_COLUMN]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Coluna obrigatória não encontrada: {column}"
            )

    # Verificação do alvo
    if df[TARGET].isna().any():
        raise ValueError(
            "A coluna isFraud contém valores ausentes."
        )

    if df[TARGET].nunique() != 2:
        raise ValueError(
            "A coluna isFraud contém valores ausentes."
        )

    # Conferência das proporções
    if abs(TRAIN_SIZE + VALIDATION_SIZE + TEST_SIZE - 1.0) > 1e-9:
        raise ValueError("As proporções de divisão devem somar 100%.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ========================================================
    # 1. DIVISÃO ESTRATIFICADA
    # ========================================================

    print("\n" + "=" * 65)
    print("1. DIVISÃO ESTRATIFICADA")
    print("=" * 65)

    # Separa 20% para teste e mantém 80% para desenvolvimento
    train_validation, test_stratified = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df[TARGET]
    )

    # Divide os 80% restantes em 60% treinamento e 20% validação
    validation_relative_size = VALIDATION_SIZE / (
        TRAIN_SIZE + VALIDATION_SIZE
    )

    train_stratified, validation_stratified = train_test_split(
        train_validation,
        test_size=validation_relative_size,
        random_state=RANDOM_STATE,
        stratify=train_validation[TARGET]
    )

    # Reinicia os índices
    train_stratified = train_stratified.reset_index(drop=True)
    validation_stratified = validation_stratified.reset_index(drop=True)
    test_stratified = test_stratified.reset_index(drop=True)

    # Exibe resultados
    display_dataset_info("Treinamento estratificado", train_stratified)
    display_dataset_info("Validação estratificada", validation_stratified)
    display_dataset_info("Teste estratificado", test_stratified)

    # Salva arquivos
    save_dataset(train_stratified, "train_stratified.csv")
    save_dataset(validation_stratified, "validation_stratified.csv")
    save_dataset(test_stratified, "test_stratified.csv")

    # ========================================================
    # 2. DIVISÃO CRONOLÓGICA
    # ========================================================

    print("\n" + "=" * 65)
    print("2. DIVISÃO CRONOLÓGICA")
    print("=" * 65)

    # Ordena os registros pelo tempo da transação
    df_chronological = df.sort_values(
        by=TIME_COLUMN,
        kind="mergesort"
    ).reset_index(drop=True)

    total_records = len(df_chronological)

    train_end = int(total_records * TRAIN_SIZE)
    validation_end = int(
        total_records * (TRAIN_SIZE + VALIDATION_SIZE)
    )

    # Separa os conjuntos mantendo a ordem temporal
    train_chronological = df_chronological.iloc[:train_end].copy()

    validation_chronological = df_chronological.iloc[
        train_end:validation_end
    ].copy()

    test_chronological = df_chronological.iloc[
        validation_end:
    ].copy()

    # Reinicia os índices
    train_chronological = train_chronological.reset_index(drop=True)
    validation_chronological = validation_chronological.reset_index(drop=True)
    test_chronological = test_chronological.reset_index(drop=True)

    # Exibe resultados
    display_dataset_info("Treinamento cronológico", train_chronological)
    display_dataset_info("Validação cronológica", validation_chronological)
    display_dataset_info("Teste cronológico", test_chronological)

    # Salva arquivos
    save_dataset(train_chronological, "train_chronological.csv")
    save_dataset(validation_chronological, "validation_chronological.csv")
    save_dataset(test_chronological, "test_chronological.csv")

    # ========================================================
    # 3. RESUMO FINAL
    # ========================================================

    print("\n" + "=" * 65)
    print("PROCESSO CONCLUÍDO")
    print("=" * 65)

    print("\nConjuntos criados:")
    print(" - train_stratified.csv")
    print(" - validation_stratified.csv")
    print(" - test_stratified.csv")
    print(" - train_chronological.csv")
    print(" - validation_chronological.csv")
    print(" - test_chronological.csv")

    print("\nOs conjuntos de teste devem permanecer reservados")
    print("até a avaliação final dos modelos.")

    print("\nProcesso finalizado com sucesso.")

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()
