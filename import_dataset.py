"""Importe un jeu de tweets annotes dans la table `tweets` (voir schema.sql).

Accepte deux formats en entree :
  - un CSV deja au format attendu : colonnes text, positive, negative
  - le format brut Sentiment140 (http://help.sentiment140.com/for-students) :
    colonnes target, ids, date, flag, user, text (sans en-tete), target valant
    0 (negatif), 2 (neutre, ignore) ou 4 (positif).

Usage :
    python import_dataset.py mocks/validation_mock.csv
    python import_dataset.py training.1600000.processed.noemoticon.csv --limit 5000
"""

from __future__ import annotations

import argparse

import pandas as pd

from db import get_engine, init_db, insert_tweets

SENTIMENT140_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]


def _from_sentiment140(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["target"].isin([0, 4])]
    return pd.DataFrame(
        {
            "text": df["text"],
            "positive": (df["target"] == 4).astype(int),
            "negative": (df["target"] == 0).astype(int),
        }
    )


def load_source(path: str) -> pd.DataFrame:
    header_probe = pd.read_csv(path, nrows=0)
    if {"text", "positive", "negative"}.issubset(header_probe.columns):
        return pd.read_csv(path)[["text", "positive", "negative"]]

    df = pd.read_csv(path, header=None, names=SENTIMENT140_COLUMNS, encoding="latin-1")
    return _from_sentiment140(df)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importe un jeu de tweets annotes dans la table tweets (MySQL)."
    )
    parser.add_argument("source", help="CSV au format text,positive,negative ou Sentiment140 brut")
    parser.add_argument("--limit", type=int, default=None, help="Nombre de lignes max a importer")
    parser.add_argument(
        "--if-exists",
        choices=["append", "replace"],
        default="append",
        help="Comportement si la table contient deja des donnees",
    )
    args = parser.parse_args()

    df = load_source(args.source)
    if args.limit is not None:
        df = df.head(args.limit)

    engine = get_engine()
    init_db(engine)
    inserted = insert_tweets(df, engine=engine, if_exists=args.if_exists)
    print(f"{inserted} tweets importes dans la table 'tweets'.")


if __name__ == "__main__":
    main()
