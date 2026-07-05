from import_dataset import load_source


def test_load_source_passthrough_format(tmp_path):
    path = tmp_path / "clean.csv"
    path.write_text("text,positive,negative\nhello,1,0\nbye,0,1\n")

    df = load_source(str(path))

    assert list(df.columns) == ["text", "positive", "negative"]
    assert len(df) == 2


def test_load_source_sentiment140_format(tmp_path):
    path = tmp_path / "raw.csv"
    # target, ids, date, flag, user, text -- sans en-tete, comme le dataset Sentiment140.
    path.write_text(
        '0,1,Mon,NO_QUERY,alice,"this is bad"\n'
        '4,2,Mon,NO_QUERY,bob,"this is good"\n'
        '2,3,Mon,NO_QUERY,carl,"neutral tweet"\n'
    )

    df = load_source(str(path))

    assert len(df) == 2  # la ligne neutre (target=2) est ignoree
    assert df[df["text"] == "this is bad"]["negative"].iloc[0] == 1
    assert df[df["text"] == "this is bad"]["positive"].iloc[0] == 0
    assert df[df["text"] == "this is good"]["positive"].iloc[0] == 1
    assert df[df["text"] == "this is good"]["negative"].iloc[0] == 0
