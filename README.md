# Sentiscope

## Evaluation du modèle (partie 4)

En attendant le vrai modèle de la partie 3, `evaluate.py` tourne sur un modèle et un jeu de validation factices (`mocks/`).

```bash
pip install -r requirements.txt
python build_mock_model.py
python evaluate.py
```

Resultats génerés : `figures/confusion_matrix_positive.png`,
`figures/confusion_matrix_negative.png`, `metrics.json`.