# Sentiscope

## Base de données (partie 2)

Schéma MySQL, import de données annotées et module de connexion réutilisable.
Voir [docs/database.md](docs/database.md) pour l'installation et l'usage.

## Evaluation du modèle (partie 4)

En attendant le vrai modèle de la partie 3, `evaluate.py` tourne sur un modèle et un jeu de validation factices (`mocks/`).

```bash
pip install -r requirements.txt
python build_mock_model.py
python evaluate.py
```

Resultats génerés : `figures/confusion_matrix_positive.png`,
`figures/confusion_matrix_negative.png`, `metrics.json`.

### Tests

```bash
python -m pytest -v
```