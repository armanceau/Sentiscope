"""Module de connexion/requetage reutilisable pour la table `tweets`.

Utilise par l'API (etudiant 1, connexion + lecture) et par le script
d'entrainement (etudiant 3, chargement des donnees annotees).

Configuration via la variable d'environnement DATABASE_URL, ex:
    mysql+pymysql://user:password@localhost:3306/sentiscope
A defaut, une URL locale par defaut est utilisee (voir DEFAULT_DATABASE_URL).
"""

from __future__ import annotations

import os
from functools import lru_cache

import pandas as pd
from sqlalchemy import Column, Integer, MetaData, SmallInteger, Table, Text, create_engine
from sqlalchemy.engine import Engine

DEFAULT_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/sentiscope"

metadata = MetaData()

tweets_table = Table(
    "tweets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", Text, nullable=False),
    Column("positive", SmallInteger, nullable=False, default=0),
    Column("negative", SmallInteger, nullable=False, default=0),
)


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


@lru_cache(maxsize=None)
def get_engine(database_url: str | None = None) -> Engine:
    return create_engine(database_url or get_database_url())


def init_db(engine: Engine | None = None) -> None:
    """Cree la table tweets si elle n'existe pas deja (idempotent)."""
    metadata.create_all(engine or get_engine())


def fetch_tweets(engine: Engine | None = None, limit: int | None = None) -> pd.DataFrame:
    """Charge la table tweets sous forme de DataFrame (colonnes id, text, positive, negative)."""
    query = "SELECT id, text, positive, negative FROM tweets"
    if limit is not None:
        query += f" LIMIT {int(limit)}"
    return pd.read_sql(query, engine or get_engine())


def insert_tweets(df: pd.DataFrame, engine: Engine | None = None, if_exists: str = "append") -> int:
    """Insere des tweets annotes dans la table tweets. df doit contenir text, positive, negative.

    La table doit deja exister (voir schema.sql ou init_db()) : if_exists ne pilote que le
    comportement sur les lignes, pas la creation du schema.
    """
    required = {"text", "positive", "negative"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes pour l'insertion : {missing}")

    engine = engine or get_engine()
    df[["text", "positive", "negative"]].to_sql("tweets", engine, if_exists=if_exists, index=False)
    return len(df)
