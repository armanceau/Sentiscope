# API d'analyse de sentiments (partie 1)

API Flask qui reçoit une liste de tweets et renvoie, pour chacun, un score de
sentiment entre **-1** (très négatif) et **1** (très positif).

La prédiction est déléguée au modèle de la partie 3 via l'interface convenue
`predict(tweet: str) -> float` (voir [`predictor.py`](../predictor.py)). Tant que
le modèle réel n'est pas figé, l'API utilise le modèle factice
`mocks/model_mock.joblib`.

## 1. Installation

```bash
pip install -r requirements.txt

# Générer le modèle factice utilisé par défaut (en attendant la partie 3)
python build_mock_model.py
```

Variables d'environnement optionnelles :

| Variable       | Défaut                      | Rôle                                            |
|----------------|-----------------------------|-------------------------------------------------|
| `MODEL_PATH`   | `mocks/model_mock.joblib`   | Chemin du modèle chargé (joblib) pour prédire.  |
| `PORT`         | `5000`                      | Port d'écoute du serveur de développement.      |

## 2. Lancer le serveur

```bash
python app.py                 # http://localhost:5000
# ou
flask --app app run           # équivalent via la CLI Flask
```

Vérifier que le service répond :

```bash
curl http://localhost:5000/health
# {"status":"ok"}
```

## 3. Endpoints

| Méthode & route  | Description                                                    |
|------------------|---------------------------------------------------------------|
| `POST /predict`  | Analyse une liste de tweets, renvoie `{tweet: score}`.        |
| `GET /health`    | Sonde de disponibilité (`{"status": "ok"}`).                  |
| `GET /`          | Petit descriptif de l'API (découverte des endpoints).         |

## 4. `POST /predict`

### Requête

- **Content-Type** : `application/json`
- **Corps** : un tableau JSON de chaînes (`string[]`).

```json
["I love this new phone", "This service is terrible", "meh whatever"]
```

> La variante `{"tweets": ["...", "..."]}` est également acceptée.

### Réponse `200 OK`

Un objet JSON associant chaque tweet à son score (∈ `[-1, 1]`). L'ordre des
tweets est préservé.

```json
{
  "I love this new phone": 1.0,
  "This service is terrible": -1.0,
  "meh whatever": 0.54
}
```

> Remarque : la réponse étant un objet `{tweet: score}`, deux tweets **identiques**
> partagent la même clé et n'apparaissent donc qu'une seule fois.

### Exemple `curl`

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '["I love this new phone", "This service is terrible", "meh whatever"]'
```

### Exemple Postman

1. Méthode **POST**, URL `http://localhost:5000/predict`.
2. Onglet **Body** → **raw** → type **JSON**.
3. Coller le tableau de tweets, puis **Send**.

### Exemple Python (`requests`)

```python
import requests

resp = requests.post(
    "http://localhost:5000/predict",
    json=["I love this new phone", "This service is terrible"],
)
print(resp.json())
```

## 5. Gestion des erreurs

Toutes les erreurs renvoient un corps JSON homogène :

```json
{"error": "message explicite"}
```

| Cas                                              | Code HTTP | Exemple de corps envoyé                         |
|--------------------------------------------------|-----------|-------------------------------------------------|
| Corps JSON manquant ou malformé                  | `400`     | `{bad`                                          |
| Corps qui n'est pas un tableau                   | `400`     | `"un simple texte"`                             |
| Liste vide                                       | `400`     | `[]`                                            |
| Élément non textuel (type incorrect)             | `400`     | `["ok", 42]`                                    |
| Tweet vide ou uniquement des espaces             | `400`     | `["   "]`                                       |
| Objet JSON sans clé `tweets`                     | `400`     | `{"foo": "bar"}`                                |
| Trop de tweets (> 1000 par requête)              | `413`     | `["tweet", ... x1001]`                          |
| Mauvaise méthode HTTP (ex. `GET /predict`)       | `405`     | —                                               |
| Route inconnue                                   | `404`     | `GET /nope`                                     |
| Modèle de sentiment indisponible                 | `503`     | fichier modèle absent                           |
| Erreur interne inattendue                        | `500`     | —                                               |

### Exemple d'erreur

```bash
curl -i -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" -d '[]'
```

```
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{"error": "La liste de tweets est vide."}
```

## 6. Tests

```bash
python -m pytest tests/test_api.py -v
```

Les tests couvrent le cas nominal, la structure de la réponse et l'ensemble des
cas d'erreur (liste vide, formats/types incorrects, JSON malformé, 404/405/413).
