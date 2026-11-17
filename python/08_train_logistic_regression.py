from pathlib import Path

import joblib
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ============================================================
# Fraud Analytics Platform
# Sprint 6 - Machine Learning
# Modelo: Regressao Logistica
# Nova divisao: Treinamento / Validacao / Teste
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"

RANDOM_STATE = 42

# ============================================================
# VARIAVEIS PREDITORAS
# ============================================================


NUMERIC_FEATURES = [
    "TransactionDT",
    "TransactionAmt",
    "dist1",
    "dist2"
]

CATEGORICAL_FEATURES = [
    "ProductCD",
    "card1",
    "card2",
    "card3",
    "card4",
    "card5",
    "card6",
    "addr1",
    "addr2",
    "P_emaildomain",
    "R_emaildomain"
]

TARGET = "isFraud"

# ============================================================
# CRIACAO DO PIPELINE
# ============================================================

def create_pipeline():
    
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler(with_mean=False))
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="constant",
                    fill_value="AUSENTE"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    min_frequency=100
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES
            )
        ]
    )

    model = LogisticRegression(
        class_weight="balanced",
        solver="liblinear",
        max_iter=1000,
        random_state=RANDOM_STATE
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model)
        ]
    )

# ============================================================
# AVALIACAO DO MODELO
# ============================================================

def evaluate_model(model, X_validation, y_validation, name):
    
    predictions = model.predict(X_validation)
    probabilities = model.predict_proba(X_validation)[:, 1]

    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_validation,
        predictions,
        zero_division=0
    )

    pr_auc = average_precision_score(
        y_validation,
        probabilities
    )

    matrix = confusion_matrix(
        y_validation,
        predictions
    )

    print("\n" + "=" * 60)
    print(f"RESULTADOS - {name}")
    print("=" * 60)

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")
    print(f"PR-AUC:    {pr_auc:.4f}")

    print("\nMatriz de confusao:")
    print(matrix)

    return {
        "Experimento": name,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1,
        "PR-AUC": pr_auc,
        "TN": int(matrix[0, 0]),
        "FP": int(matrix[0, 1]),
        "FN": int(matrix[1, 0]),
        "TP": int(matrix[1, 1]),
    }

# ============================================================
# EXECUCAO DE CADA EXPERIMENTO
# ============================================================

def run_experiment(train_file, validation_file, name):

    print("\n" + "#" * 60)
    print(f"EXPERIMENTO: {name}")
    print("#" * 60)

    train_df = pd.read_csv(DATA_DIR / train_file)
    validation_df = pd.read_csv(DATA_DIR / validation_file)

    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    missing_columns = [
        col for col in features + [TARGET]
        if col not in train_df.columns
        or col not in validation_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colunas ausentes: {missing_columns}"
        )

    X_train = train_df[features].copy()
    y_train = train_df[TARGET].astype(int)

    X_validation = validation_df[features].copy()
    y_validation = validation_df[TARGET].astype(int)

    # Padronizar variaveis categoricas como texto,
    # preservando valores ausentes para imputacao

    for col in CATEGORICAL_FEATURES:

        X_train[col] = (
            X_train[col]
            .astype(object)
            .where(X_train[col].notna(), np.nan)
            .map(
                lambda value:
                str(value) if pd.notna(value) else np.nan
            )
        )

        X_validation[col] = (
            X_validation[col]
            .astype(object)
            .where(X_validation[col].notna(), np.nan)
            .map(
                lambda value:
                str(value) if pd.notna(value) else np.nan
            )
        )

    print(f"\nRegistros de treinamento: {len(X_train):,}")
    print(f"Registros de validacao: {len(X_validation):,}")
    print(f"Features utilizadas: {len(features)}")


    # Criar e treinar o modelo

    pipeline = create_pipeline()

    print("\nTreinando modelo...")
    pipeline.fit(X_train, y_train)

    print("Treinamento concluido.")

    # Avaliar modelo

    results = evaluate_model(
        pipeline,
        X_validation,
        y_validation,
        name
    )

    # Salvar modelo

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_path = (
        MODEL_DIR / 
        f"logistic_holdout_{name}.joblib"
    )

    joblib.dump(pipeline, model_path)

    print(f"\nModelo salvo em: {model_path}")

    return results

# ============================================================
# PROCESSO PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("Fraud Analytics Platform")
    print("Logistic Regression - Nova divisao")
    print("=" * 60)

    experiments = [
        (
            "train_stratified.csv",
            "validation_stratified.csv",
            "stratified"
        ),
        (
            "train_chronological.csv",
            "validation_chronological.csv",
            "chronological"
        )
    ]

    results = []

    for train_file, validation_file, name in experiments:

        result = run_experiment(
            train_file,
            validation_file,
            name
        )

        results.append(result)

    # Consolidar resultados

    results_df = pd.DataFrame(results)

    results_path = (
        DATA_DIR /
        "logistic_holdout_results.csv"
    )

    results_df.to_csv(results_path, index=False)

    print("\n" + "=" * 60)
    print("COMPARACAO DOS EXPERIMENTOS")
    print("=" * 60)

    print(results_df.to_string(index=False))

    print(f"\nResultados salvos em: {results_path}")
    print("\nProcesso concluido com sucesso.")


if __name__ == "__main__":
    main()