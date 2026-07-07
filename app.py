"""Point d'entree de l'API Flask d'analyse de sentiments (etudiant 1).

Lancement en local :
    python app.py                 # serveur de dev sur http://localhost:5000
    flask --app app run           # alternative via la CLI Flask

Endpoint principal : POST /predict (voir routes.py et docs/api.md).
"""

from __future__ import annotations

import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from routes import api


def create_app() -> Flask:
    """Fabrique l'application Flask (pratique pour les tests et le deploiement)."""
    app = Flask(__name__)
    app.register_blueprint(api)

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        # Renvoie les erreurs HTTP (404, 405, ...) en JSON plutot qu'en page HTML.
        return jsonify({"error": exc.description}), exc.code

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        # Filet de securite : toute erreur imprevue devient un 500 JSON propre.
        return jsonify({"error": "Erreur interne du serveur."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
