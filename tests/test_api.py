import pytest

import predictor
from app import create_app
from mocks.mock_model import build_and_save


@pytest.fixture(scope="module", autouse=True)
def mock_model():
    # Genere mocks/model_mock.joblib et vide le cache de chargement pour que
    # l'API predise via le modele factice (interface predict(tweet) -> float).
    build_and_save()
    predictor.get_model.cache_clear()
    yield
    predictor.get_model.cache_clear()


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_predict_returns_a_score_per_tweet(client):
    resp = client.post(
        "/predict", json=["I love this great day", "I hate this awful thing"]
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert set(data) == {"I love this great day", "I hate this awful thing"}
    assert data["I love this great day"] > 0
    assert data["I hate this awful thing"] < 0
    for score in data.values():
        assert -1.0 <= score <= 1.0


def test_predict_accepts_tweets_object_form(client):
    resp = client.post("/predict", json={"tweets": ["hello good world"]})
    assert resp.status_code == 200
    assert "hello good world" in resp.get_json()


def test_empty_list_returns_400(client):
    resp = client.post("/predict", json=[])
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_body_not_a_list_returns_400(client):
    resp = client.post("/predict", json="just a string")
    assert resp.status_code == 400


def test_non_string_element_returns_400(client):
    resp = client.post("/predict", json=["ok tweet", 123])
    assert resp.status_code == 400


def test_blank_tweet_returns_400(client):
    resp = client.post("/predict", json=["   "])
    assert resp.status_code == 400


def test_object_without_tweets_key_returns_400(client):
    resp = client.post("/predict", json={"foo": "bar"})
    assert resp.status_code == 400


def test_malformed_json_returns_400(client):
    resp = client.post("/predict", data="{not valid json", content_type="application/json")
    assert resp.status_code == 400


def test_too_many_tweets_returns_413(client):
    resp = client.post("/predict", json=["tweet"] * 1001)
    assert resp.status_code == 413


def test_get_on_predict_is_405_json(client):
    resp = client.get("/predict")
    assert resp.status_code == 405
    assert "error" in resp.get_json()


def test_unknown_route_returns_404_json(client):
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    assert "error" in resp.get_json()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
