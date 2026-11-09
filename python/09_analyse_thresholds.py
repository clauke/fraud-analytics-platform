from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)


# ============================================================
# Fraud Analytics Platform
# Sprint 6 - Machine Learning
# Análise dos limiares de classificação
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"

TARGET = "isFraud"

THRESHOLDS = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]

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

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

def prepare_features(df):

    X = df[FEATURES].copy()

    # Padronizar variaveis categoricas da mesma forma
    # utilizada durante o treinamento
    for col in CATEGORICAL_FEATURES:
        X[col] = (
            X[col]
            .astype(object)
            .where(X[col].notna(), np.nan)
            .map(
                lambda value:
                str(value) if pd.notna(value) else np.nan
            )
        )

    return X

def analyze_thresholds(model, validation_df, experiment_name):

    X_validation = prepare_features(validation_df)
    y_validation = validation_df[TARGET].astype(int)

    # Obter probabilidades de fraude
    probabilities = model.predict_proba(X_validation)[:, 1]

    results = []

    print("\n" + "=" * 75)
    print(f"ANALISE DE LIMIARES - {experiment_name}")
    print("=" * 75)

    for threshold in THRESHOLDS:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_validation,
            predictions,
            labels=[0, 1]
        ).ravel()

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

        results.append({
            "Experimento": experiment_name,
            "Threshold": threshold,
            "Precision": precision,
            "Recall": recall,
            "F1-score": f1,
            "PR-AUC": average_precision_score(
                y_validation,
                probabilities
            ),
            "True_Positive": tp,
            "True_Negative": tn,
            "False_Positive": fp,
            "False_Negative": fn
        })

    results_df = pd.DataFrame(results)

    print(
        results_df[
            [
                "Threshold",
                "Precision",
                "Recall",
                "F1-score",
                "False_Positive",
                "False_Negative"
            ]
        ].to_string(
            index=False,
            formatters={
                "Precision": "{:.4f}".format,
                "Recall": "{:.4f}".format,
                "F1-score": "{:.4f}".format
            }
        )
    )

    return results_df

def main():

    print("=" * 75)
    print("Fraud Analytics Platform")
    print("Analise dos limiares de classificacao")
    print("=" * 75)

    experiments = [
        {
            "name": "stratified",
            "model_file": "baseline_logistic_stratified.joblib",
            "validation_file": "fraud_validation_stratified.csv"
        },
        {
            "name": "chronological",
            "model_file": "baseline_logistic_chronological.joblib",
            "validation_file": "fraud_validation_chronological.csv"
        }
    ]

    all_results = []

    for experiment in experiments:

        model_path = MODEL_DIR / experiment["model_file"]
        validation_path = DATA_DIR / experiment["validation_file"]

        if not model_path.exists():
            raise FileNotFoundError(
                f"Modelo nao encontrado: {model_path}"
            )

        if not validation_path.exists():
            raise FileNotFoundError(
                f"Dataset nao encontrado: {validation_path}"
            )

        print(
            f"\nCarregando modelo: {experiment['model_file']}"
        )

        model = joblib.load(model_path)

        validation_df = pd.read_csv(validation_path)

        results_df = analyze_thresholds(
            model,
            validation_df,
            experiment["name"]
        )

        all_results.append(results_df)

    # Consolidar resultados

    final_results = pd.concat(
        all_results,
        ignore_index=True
    )

    output_file = DATA_DIR / "threshold_analysis_results.csv"

    final_results.to_csv(
        output_file,
        index=False
    )

    print("\n" + "=" * 75)
    print("ANALISE CONCLUIDA")
    print("=" * 75)

    print(f"\nArquivo gerado: {output_file}")

    print(
        "\nTotal de combinacoes avaliadas:",
        len(final_results)
    )

if __name__ == "__main__":
    main()
        