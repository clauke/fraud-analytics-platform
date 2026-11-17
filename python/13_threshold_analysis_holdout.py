from pathlib import Path
import gc

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    confusion_matrix
)

# ============================================================
# CONFIGURACOES
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data" / "processed"
MODELS_DIR = ROOT_DIR / "models"

TARGET = "isFraud"

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

THRESHOLDS = np.round(
    np.arange(0.10, 0.91, 0.05),
    2
)

# ============================================================
# PREPARACAO DOS DADOS
# ============================================================

def load_validation_data(experiment):

    file_path = DATA_DIR / f"validation_{experiment}.csv"

    print(f"\nCarregando validacao: {file_path.name}")

    df = pd.read_csv(file_path)

    if TARGET not in df.columns:
        raise ValueError(
            f"Coluna alvo '{TARGET}' nao encontrada."
        )

    missing_features = [
        col for col in FEATURES
        if col not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Features ausentes: {missing_features}"
        )

    y = df[TARGET].copy()

    X = df[FEATURES].copy()

    # Garante tratamento consistente das variaveis categoricas
    for col in CATEGORICAL_FEATURES:
        X[col] = X[col].fillna("AUSENTE").astype(str)

    print(f"Registros de validacao: {len(df):,}")
    print(f"Features utilizadas: {len(FEATURES)}")
    print(f"Fraudes: {int(y.sum()):,}")

    return X, y

# ============================================================
# ANALISE DOS LIMIARES
# ============================================================

def analyze_thresholds(
    model,
    X,
    y,
    model_name,
    experiment
):

    print("\nCalculando probabilidades...")

    probabilities = model.predict_proba(X)[:, 1]

    pr_auc = average_precision_score(
        y,
        probabilities
    )

    print(f"PR-AUC: {pr_auc:.4f}")

    results = []

    for threshold in THRESHOLDS:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y,
            predictions,
            zero_division=0
        )

        tn, fp, fn, tp = confusion_matrix(
            y,
            predictions,
            labels=[0, 1]
        ).ravel()

        results.append({
            "Experimento": experiment,
            "Modelo": model_name,
            "Threshold": threshold,
            "Precision": precision,
            "Recall": recall,
            "F1-score": f1,
            "PR-AUC": pr_auc,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "TP": tp
        })

    return results

# ============================================================
# EXECUCAO DOS EXPERIMENTOS
# ============================================================

def run_experiment(
    model_name,
    experiment,
    model_file
):

    print("\n" + "#" * 60)
    print(f"MODELO: {model_name}")
    print(f"EXPERIMENTO: {experiment}")
    print("#" * 60)

    model_path = MODELS_DIR / model_file

    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo nao encontrado: {model_path}"
        )

    print(f"\nCarregando modelo: {model_file}")

    model = joblib.load(model_path)

    X, y = load_validation_data(experiment)

    results = analyze_thresholds(
        model=model,
        X=X,
        y=y,
        model_name=model_name,
        experiment=experiment
    )

    del model
    del X
    del y

    gc.collect()

    return results

# ============================================================
# RESUMO DOS MELHORES LIMIARES
# ============================================================

def show_best_thresholds(df):

    print("\n" + "=" * 60)
    print("MELHORES LIMIARES POR F1-SCORE")
    print("=" * 60)

    for (experiment, model), group in df.groupby(
        ["Experimento", "Modelo"]
    ):

        best = group.loc[group["F1-score"].idxmax()]

        print(f"\nExperimento: {experiment}")
        print(f"Modelo: {model}")
        print(f"Threshold: {best['Threshold']:.2f}")
        print(f"Precision: {best['Precision']:.4f}")
        print(f"Recall: {best['Recall']:.4f}")
        print(f"F1-score: {best['F1-score']:.4f}")
        print(f"PR-AUC: {best['PR-AUC']:.4f}")
        print(f"FP: {int(best['FP']):,}")
        print(f"FN: {int(best['FN']):,}")

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("Fraud Analytics Platform")
    print("Analise de Thresholds - Holdout 60/20/20")
    print("=" * 60)

    all_results = []

    experiments = [
        {
            "model_name": "Logistic Regression",
            "experiment": "stratified",
            "model_file": "logistic_holdout_stratified.joblib"
        },
        {
            "model_name": "Logistic Regression",
            "experiment": "chronological",
            "model_file": "logistic_holdout_chronological.joblib"
        },
        {
            "model_name": "Random Forest",
            "experiment": "stratified",
            "model_file": "random_forest_holdout_stratified.joblib"
        },
        {
            "model_name": "Random Forest",
            "experiment": "chronological",
            "model_file": "random_forest_holdout_chronological.joblib"
        }
    ]

    for config in experiments:

        results = run_experiment(
            model_name=config["model_name"],
            experiment=config["experiment"],
            model_file=config["model_file"]
        )

        all_results.extend(results)

    # Consolidacao
    df_results = pd.DataFrame(all_results)

    # Ordenacao para facilitar a analise
    df_results = df_results.sort_values(
        by=["Experimento", "Modelo", "Threshold"]
    ).reset_index(drop=True)

     # Salvamento
    output_file = (
        DATA_DIR / "threshold_analysis_holdout_results.csv"
    )

    df_results.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 60)
    print("RESUMO DA ANALISE")
    print("=" * 60)

    print(
        df_results[
            [
                "Experimento",
                "Modelo",
                "Threshold",
                "Precision",
                "Recall",
                "F1-score",
                "FP",
                "FN"
            ]
        ].to_string(index=False)
    )

    show_best_thresholds(df_results)

    print("\n" + "=" * 60)
    print("ANALISE CONCLUIDA")
    print("=" * 60)

    print(f"\nResultados salvos em: {output_file}")


if __name__ == "__main__":
    main()
