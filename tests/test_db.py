import pandas as pd
import pytest
from sqlalchemy import create_engine

from db import fetch_tweets, init_db, insert_tweets


@pytest.fixture
def engine():
    # SQLite en memoire : meme API SQLAlchemy que MySQL, sans dependance externe pour les tests.
    return create_engine("sqlite:///:memory:")


def test_init_db_creates_table(engine):
    init_db(engine)

    df = fetch_tweets(engine)

    assert list(df.columns) == ["id", "text", "positive", "negative"]
    assert len(df) == 0


def test_insert_then_fetch_roundtrip(engine):
    init_db(engine)
    rows = pd.DataFrame(
        {
            "text": ["I love this", "I hate this"],
            "positive": [1, 0],
            "negative": [0, 1],
        }
    )

    inserted = insert_tweets(rows, engine=engine)

    assert inserted == 2
    df = fetch_tweets(engine)
    assert len(df) == 2
    assert set(df["text"]) == {"I love this", "I hate this"}


def test_insert_tweets_rejects_missing_columns(engine):
    init_db(engine)
    rows = pd.DataFrame({"text": ["hello"], "positive": [1]})

    with pytest.raises(ValueError):
        insert_tweets(rows, engine=engine)
