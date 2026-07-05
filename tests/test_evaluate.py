import joblib
import pytest

from evaluate import evaluate, load_model, load_validation_data, predict_labels
from mocks.mock_model import build_and_save


class ConstantModel:
    """Modele factice renvoyant toujours le même score, pour tester le seuillage."""

    def __init__(self, score: float):
        self.score = score

    def predict(self, tweet: str) -> float:
        return self.score


@pytest.mark.parametrize(
    "score, expected_positive, expected_negative",
    [
        (0.5, 1, 0),
        (-0.5, 0, 1),
        (0.0, 0, 0),
    ],
)
def test_predict_labels_thresholding(score, expected_positive, expected_negative):
    positive, negative = predict_labels(ConstantModel(score), ["un tweet"])
    assert positive == [expected_positive]
    assert negative == [expected_negative]


def test_load_validation_data_ok(tmp_path):
    path = tmp_path / "validation.csv"
    path.write_text("text,positive,negative\nhello,1,0\n")

    df = load_validation_data(str(path))

    assert list(df.columns) == ["text", "positive", "negative"]
    assert len(df) == 1


def test_load_validation_data_missing_columns(tmp_path):
    path = tmp_path / "validation.csv"
    path.write_text("text,positive\nhello,1\n")

    with pytest.raises(ValueError):
        load_validation_data(str(path))


def test_load_model_rejects_object_without_predict(tmp_path):
    path = tmp_path / "not_a_model.joblib"
    joblib.dump(object(), path)

    with pytest.raises(TypeError):
        load_model(str(path))


def test_evaluate_end_to_end_with_mock_model():
    build_and_save()

    metrics = evaluate("mocks/model_mock.joblib", "mocks/validation_mock.csv")

    assert set(metrics) == {"positive", "negative"}
    for label in ("positive", "negative"):
        assert metrics[label]["1"]["recall"] == pytest.approx(1.0)
        assert metrics[label]["1"]["precision"] == pytest.approx(0.75)
