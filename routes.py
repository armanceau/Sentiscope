"""Endpoints HTTP de l'API d'analyse de sentiments (etudiant 1).

Endpoint principal : POST /predict
  Entree  : un tableau JSON de tweets (string[]), ex. ["j'adore", "je deteste"]
            (le format {"tweets": [...]} est aussi accepte).
  Sortie  : un objet JSON {tweet: score}, score entre -1 (tres negatif) et
            1 (tres positif).

La prediction est deleguee a predictor.predict, qui fait le pont avec le modele
de l'etudiant 3 (voir predictor.py).
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from predictor import predict

api = Blueprint("api", __name__)

# Garde-fou contre les requetes trop volumineuses.
MAX_TWEETS = 1000


def _error(message: str, status: int):
    """Reponse d'erreur JSON homogene : {"error": "..."}."""
    return jsonify({"error": message}), status


@api.get("/")
def index():
    """Petit point d'entree de decouverte de l'API."""
    return jsonify(
        {
            "service": "Sentiscope - API d'analyse de sentiments",
            "endpoints": {
                "POST /predict": "Analyse une liste de tweets et renvoie {tweet: score}",
                "GET /health": "Verification de disponibilite",
            },
        }
    )


@api.get("/health")
def health():
    """Sonde de disponibilite (utile pour le monitoring / CI)."""
    return jsonify({"status": "ok"})


@api.post("/predict")
def predict_sentiments():
    # force=True : on parse le corps en JSON meme si le Content-Type est absent
    # ou incorrect ; silent=True : None au lieu d'une exception si non parseable.
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return _error(
            "Corps de requete JSON invalide ou manquant. Envoyez un tableau JSON de tweets.",
            400,
        )

    # On accepte le tableau brut ["tweet", ...] (format des consignes) ou la
    # variante pratique {"tweets": [...]}.
    if isinstance(payload, dict):
        if "tweets" not in payload:
            return _error(
                'Objet JSON sans cle "tweets". Envoyez un tableau de tweets ou {"tweets": [...]}.',
                400,
            )
        tweets = payload["tweets"]
    else:
        tweets = payload

    if not isinstance(tweets, list):
        return _error("Le corps doit etre un tableau JSON de chaines (string[]).", 400)

    if len(tweets) == 0:
        return _error("La liste de tweets est vide.", 400)

    if len(tweets) > MAX_TWEETS:
        return _error(
            f"Trop de tweets ({len(tweets)}) : maximum {MAX_TWEETS} par requete.",
            413,
        )

    for i, tweet in enumerate(tweets):
        if not isinstance(tweet, str):
            return _error(
                f"Element a l'index {i} invalide : chaque tweet doit etre une chaine de caracteres.",
                400,
            )
        if not tweet.strip():
            return _error(
                f"Element a l'index {i} invalide : le tweet est vide.",
                400,
            )

    try:
        # dict {tweet: score} : conforme au format de reponse attendu. Des tweets
        # identiques fusionnent naturellement sur une meme cle.
        scores = {tweet: predict(tweet) for tweet in tweets}
    except FileNotFoundError:
        return _error(
            "Modele de sentiment indisponible : generez-le (python build_mock_model.py) "
            "ou definissez la variable d'environnement MODEL_PATH.",
            503,
        )

    return jsonify(scores)
