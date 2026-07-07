"""Genere mocks/model_mock.joblib, utilise par les tests et comme modele par
defaut de l'API (app.py/predictor.py) quand MODEL_PATH n'est pas defini.
Voir mocks/mock_model.py pour les details.
"""

from mocks.mock_model import build_and_save

if __name__ == "__main__":
    saved_path = build_and_save()
    print(f"Modele factice sauvegarde : {saved_path}")
