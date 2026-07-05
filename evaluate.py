from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# TODO: remplacer par le vrai modele de la aprtie 3 des que son format est figé
DEFAULT_MODEL_PATH = "mocks/model_mock.joblib"
# TODO: remplacer par le vrai jeu de validation (issu de db.py / table tweets)
DEFAULT_DATA_PATH = "mocks/validation_mock.csv"
FIGURES_DIR = Path("figures")
SCORE_THRESHOLD = 0.0  # seuil pour binariser le score continu en positive/negative


def load_model(model_path: str):
    model = joblib.load(model_path)
    if not hasattr(model, "predict"):
        raise TypeError(
            f"L'objet charge depuis {model_path} n'expose pas predict(tweet: str) -> float."
        )
    return model


def load_validation_data(data_path: str) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    required_columns = {"text", "positive", "negative"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans {data_path} : {missing}")
    return df


def predict_labels(model, texts: list[str]) -> tuple[list[int], list[int]]:
    scores = [model.predict(t) for t in texts]
    predicted_positive = [1 if s > SCORE_THRESHOLD else 0 for s in scores]
    predicted_negative = [1 if s < -SCORE_THRESHOLD else 0 for s in scores]
    return predicted_positive, predicted_negative


def plot_confusion_matrix(y_true, y_pred, label: str, output_path: Path) -> None:
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Predit 0", "Predit 1"],
        yticklabels=["Reel 0", "Reel 1"],
    )
    plt.title(f"Matrice de confusion - classe {label}")
    plt.ylabel("Reel")
    plt.xlabel("Predit")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()


def evaluate(model_path: str, data_path: str) -> dict:
    model = load_model(model_path)
    df = load_validation_data(data_path)

    predicted_positive, predicted_negative = predict_labels(model, df["text"].tolist())

    metrics = {}
    for label, y_true, y_pred in (
        ("positive", df["positive"].tolist(), predicted_positive),
        ("negative", df["negative"].tolist(), predicted_negative),
    ):
        report = classification_report(
            y_true, y_pred, labels=[0, 1], output_dict=True, zero_division=0
        )
        metrics[label] = report
        plot_confusion_matrix(y_true, y_pred, label, FIGURES_DIR / f"confusion_matrix_{label}.png")

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evalue le modele de sentiment (metriques + matrices de confusion)."
    )
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, help="Chemin vers le modele sauvegarde")
    parser.add_argument(
        "--data", default=DEFAULT_DATA_PATH, help="Chemin vers le CSV de validation (text, positive, negative)"
    )
    parser.add_argument("--output", default="metrics.json", help="Fichier JSON de sortie pour les metriques")
    args = parser.parse_args()

    metrics = evaluate(args.model, args.data)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    for label in ("positive", "negative"):
        report = metrics[label]
        print(f"--- Classe {label} ---")
        print(f"  precision (1) : {report['1']['precision']:.2f}")
        print(f"  rappel    (1) : {report['1']['recall']:.2f}")
        print(f"  f1-score  (1) : {report['1']['f1-score']:.2f}")

    print(f"\nMatrices de confusion sauvegardees dans {FIGURES_DIR}/")
    print(f"Metriques detaillees sauvegardees dans {args.output}")


if __name__ == "__main__":
    main()
