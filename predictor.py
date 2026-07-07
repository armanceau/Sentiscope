"""Interface de prediction consommee par l'API Flask (etudiant 1).

Fait le pont avec le modele de sentiment de l'etudiant 3 : charge le modele
sauvegarde (joblib) et expose la fonction convenue lors du cadrage des
interfaces :

    predict(tweet: str) -> float   # score entre -1 (tres negatif) et 1 (tres positif)

Par defaut, charge le modele factice `mocks/model_mock.joblib` (voir
build_mock_model.py), pratique pour developper/tester sans entrainer un vrai
modele. Le chemin est configurable via la variable d'environnement MODEL_PATH,
pour basculer vers le vrai modele entraine par model.py (ex. models/sentiment_model.joblib).
"""

from __future__ import annotations

import os
from functools import lru_cache

import joblib

DEFAULT_MODEL_PATH = "mocks/model_mock.joblib"


def get_model_path() -> str:
    return os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH)


@lru_cache(maxsize=None)
def get_model(model_path: str | None = None):
    """Charge (et met en cache) le modele de sentiment.

    Le modele doit exposer predict(tweet: str) -> float (interface etudiant 3).
    Leve FileNotFoundError si le fichier n'existe pas, TypeError si l'objet
    charge n'a pas la bonne interface.
    """
    path = model_path or get_model_path()
    model = joblib.load(path)
    if not hasattr(model, "predict"):
        raise TypeError(
            f"L'objet charge depuis {path} n'expose pas predict(tweet: str) -> float."
        )
    return model


def predict(tweet: str) -> float:
    """Retourne le score de sentiment d'un tweet, borne dans [-1, 1]."""
    score = float(get_model().predict(tweet))
    return max(-1.0, min(1.0, score))
