# Sentiscope

## API d'analyse de sentiments (partie 1)

API Flask exposant un endpoint `POST /predict` qui reçoit un tableau de tweets
et renvoie `{tweet: score}` (score entre -1 et 1). Voir
[docs/api.md](docs/api.md) pour l'installation, les exemples de requêtes
(curl/Postman) et la gestion des erreurs.

```bash
pip install -r requirements.txt
python build_mock_model.py     # modele factice pour tester l'API sans entrainer un vrai modele
python app.py                  # http://localhost:5000

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '["I love this", "This is terrible"]'
```

## Base de données (partie 2)

Schéma MySQL, import de données annotées et module de connexion réutilisable.
Voir [docs/database.md](docs/database.md) pour l'installation et l'usage.

## Machine Learning & Réentraînement (partie 3)

Entraînement d'un modèle de régression logistique avec `scikit-learn` pour analyser le sentiment des tweets.
Le modèle apprend depuis les données de la base MySQL et est planifié pour être ré-entraîné automatiquement de façon hebdomadaire.

```bash
# Entraînement manuel du modèle (génère models/sentiment_model.joblib)
python model.py --model-path models/sentiment_model.joblib
```

**Important :** Par défaut, l'API (`app.py`/`predictor.py`) charge un modèle factice
(`mocks/model_mock.joblib`), pratique pour développer/tester sans avoir à entraîner un vrai
modèle. `evaluate.py`, lui, charge par défaut le vrai modèle (voir partie 4). Pour faire tourner
l'API avec le vrai modèle entraîné, définissez la variable d'environnement `MODEL_PATH` avant de
lancer `app.py` :

```bash
export MODEL_PATH="models/sentiment_model.joblib"
python app.py
```

Voir [CRONTAB_INSTRUCTIONS.md](CRONTAB_INSTRUCTIONS.md) pour configurer le réentraînement automatique.

## Evaluation du modèle (partie 4)

`evaluate.py` charge le modèle réel entraîné par `model.py` (variable `MODEL_PATH`, comme pour
`app.py`) et le jeu de validation directement depuis la table `tweets` (variable `DATABASE_URL`,
voir [docs/database.md](docs/database.md)) :

```bash
export DATABASE_URL="mysql+pymysql://root:root@localhost:3306/sentiscope"
export MODEL_PATH="models/sentiment_model.joblib"
python evaluate.py
```

Un CSV de validation (`text,positive,negative`) peut être fourni en alternative avec `--data`,
par exemple pour un jeu de validation tenu à l'écart de l'entraînement.

Resultats génerés : `figures/confusion_matrix_positive.png`,
`figures/confusion_matrix_negative.png`, `metrics.json`.

### Rapport PDF

Le rapport final (`rapport_evaluation.pdf`) est généré à partir de la source éditable
`rapport_evaluation.md` (matrices de confusion, précision/rappel/F1-score, analyse des biais,
recommandations), pour rester facile à corriger sans toucher au PDF directement :

```bash
pip install markdown xhtml2pdf
python generate_report.py     # lit rapport_evaluation.md -> ecrit rapport_evaluation.pdf
```

À lancer après `evaluate.py`, puisque le rapport embarque les figures qu'il génère.

### Tests

```bash
python -m pytest -v
```