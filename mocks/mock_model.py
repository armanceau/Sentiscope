"""
Modele factice, a remplacer par le vrai modele de l'etudiant 3 (LogisticRegression
+ TF-IDF) des que son format de sauvegarde sera fige. Respecte l'interface
convenue predict(tweet: str) -> float (score entre -1 et 1).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import joblib

POSITIVE_WORDS = {"love", "great", "happy", "good", "excellent", "amazing"}
NEGATIVE_WORDS = {"hate", "bad", "terrible", "sad", "awful", "worst"}


class MockSentimentModel:
    def predict(self, tweet: str) -> float:
        words = set(tweet.lower().split())
        pos_hits = len(words & POSITIVE_WORDS)
        neg_hits = len(words & NEGATIVE_WORDS)

        if pos_hits or neg_hits:
            score = (pos_hits - neg_hits) / (pos_hits + neg_hits)
        else:
            digest = hashlib.sha256(tweet.encode("utf-8")).hexdigest()
            score = (int(digest[:8], 16) / 0xFFFFFFFF) * 2 - 1

        return max(-1.0, min(1.0, score))


def build_and_save(path: str | Path = "mocks/model_mock.joblib") -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(MockSentimentModel(), path)
    return path
