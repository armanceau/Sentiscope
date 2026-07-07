import argparse
import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from db import fetch_tweets


class SentimentModel:
    """Modele de sentiment (Logistic Regression + TF-IDF) encapsulant la logique
    scikit-learn et exposant la methode predict(tweet) attendue.
    """

    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=10000)),
            ("clf", LogisticRegression(random_state=42))
        ])

    def fit(self, X, y):
        self.pipeline.fit(X, y)
        return self

    def predict(self, tweet: str) -> float:
        """Retourne le score de sentiment dans l'intervalle [-1, 1]."""
        proba = self.pipeline.predict_proba([tweet])[0]
        # Recherche de l'index de la classe positive (1)
        classes = list(self.pipeline.classes_)
        if 1 in classes:
            pos_idx = classes.index(1)
            score = 2 * proba[pos_idx] - 1
        else:
            # S'il n'y a pas de classe 1 (ex: donnees avec une seule classe), renvoyer 0
            score = 0.0
        return float(score)


def train_and_save_model(model_path="model.joblib", limit=None, engine=None):
    """Entraine le modele sur les tweets de la base de donnees et le sauvegarde."""
    print("Chargement des donnees...")
    df = fetch_tweets(engine=engine, limit=limit)
    
    # Filtrage des tweets valides (qui ont au moins un label positif ou negatif)
    df = df[(df["positive"] == 1) | (df["negative"] == 1)]
    if len(df) == 0:
        raise ValueError("Aucune donnee d'entrainement trouvee.")
        
    print(f"{len(df)} tweets charges pour l'entrainement.")
    
    # La target est 1 si le tweet est positif, 0 s'il est negatif
    y = df["positive"].astype(int)
    X = df["text"]
    
    model = SentimentModel()
    print("Entrainement en cours...")
    model.fit(X, y)
    
    print(f"Sauvegarde du modele vers {model_path}...")
    os.makedirs(os.path.dirname(os.path.abspath(model_path)), exist_ok=True)
    joblib.dump(model, model_path)
    print("Termine.")
    return model


if __name__ == "__main__":
    # Import the module itself to fix class serialization issues with joblib
    import model
    import argparse
    parser = argparse.ArgumentParser(description="Entraine le modele de sentiment (Logistic Regression)")
    parser.add_argument("--model-path", default="model.joblib", help="Chemin de sauvegarde du modele")
    parser.add_argument("--limit", type=int, default=None, help="Nombre max de tweets a utiliser")
    args = parser.parse_args()
    
    model.train_and_save_model(args.model_path, limit=args.limit)
