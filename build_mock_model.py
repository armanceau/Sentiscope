"""Genere mocks/model_mock.joblib pour pouvoir lancer evaluate.py sans attendre
le modele reel de l'etudiant 3. Voir mocks/mock_model.py pour les details.
"""

from mocks.mock_model import build_and_save

if __name__ == "__main__":
    saved_path = build_and_save()
    print(f"Modele factice sauvegarde : {saved_path}")
