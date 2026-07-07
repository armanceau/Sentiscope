# Sentiscope

## API d'analyse de sentiments (partie 1)

API Flask exposant un endpoint `POST /predict` qui reçoit un tableau de tweets
et renvoie `{tweet: score}` (score entre -1 et 1). Voir
[docs/api.md](docs/api.md) pour l'installation, les exemples de requêtes
(curl/Postman) et la gestion des erreurs.

```bash
pip install -r requirements.txt
python build_mock_model.py     # modèle factice en attendant la partie 3
python app.py                  # http://localhost:5000

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '["I love this", "This is terrible"]'
```

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