# Base de données (partie 2)

Stockage des tweets annotés utilisés pour entraîner (étudiant 3) et évaluer
(étudiant 4) le modèle, et consommés par l'API (étudiant 1).

## 1. Installer et démarrer MySQL

Sur une machine locale (Linux/Mac/WSL) :

```bash
sudo apt install mysql-server   # ou brew install mysql sur Mac
sudo service mysql start
```

Ou via Docker :

```bash
docker run --name sentiscope-mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8
```

## 2. Créer la base et la table

```bash
mysql -u root -p < schema.sql
```

Cela crée la base `sentiscope` et la table `tweets` (`id`, `text`, `positive`, `negative`).

## 3. Configurer la connexion

Le module [`db.py`](../db.py) lit l'URL de connexion depuis la variable
d'environnement `DATABASE_URL` (format SQLAlchemy) :

```bash
export DATABASE_URL="mysql+pymysql://root:root@localhost:3306/sentiscope"
```

Sans cette variable, `db.py` utilise par défaut
`mysql+pymysql://root:root@localhost:3306/sentiscope`.

## 4. Importer des données annotées

Un petit jeu de test est disponible dans `mocks/validation_mock.csv` (déjà au
format `text,positive,negative`) :

```bash
python import_dataset.py mocks/validation_mock.csv
```

Pour un vrai volume d'entraînement, le dataset public
[Sentiment140](http://help.sentiment140.com/for-students) (1.6M tweets
annotés positif/négatif) est directement supporté : téléchargez
`training.1600000.processed.noemoticon.csv` puis lancez :

```bash
python import_dataset.py training.1600000.processed.noemoticon.csv --limit 50000
```

`import_dataset.py` détecte automatiquement le format (colonnes
`text,positive,negative` ou format brut Sentiment140 avec `target` 0/2/4) et
convertit vers le schéma de la table `tweets`.

## 5. Utiliser le module `db.py` depuis un autre script

```python
from db import get_engine, fetch_tweets, insert_tweets

engine = get_engine()
df = fetch_tweets(engine)          # DataFrame text/positive/negative pour l'entrainement
insert_tweets(new_rows_df, engine) # ajout de nouvelles annotations
```
