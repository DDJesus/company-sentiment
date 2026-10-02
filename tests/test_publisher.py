import json

from datetime import date, datetime
from pathlib import Path

from company_sentiment.models import BatchType
from company_sentiment.publisher import publish_batch


def test_publish_batch_creates_expected_file(
    tmp_path: Path,
):
    output_path = publish_batch(
        market_date=date(2026, 10, 2),
        batch_type=BatchType.PREMARKET,
        output_dir=tmp_path,
        seed=42,
    )

    assert output_path.exists()
    assert output_path.name == (
        "sentiment-2026-10-02-premarket.json"
    )


def test_published_batch_has_expected_metadata(
    tmp_path: Path,
):
    output_path = publish_batch(
        market_date=date(2026, 10, 2),
        batch_type=BatchType.PREMARKET,
        output_dir=tmp_path,
        seed=42,
    )

    payload = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    assert payload["schema_version"] == (
        "company.sentiment.batch/v1"
    )
    assert payload["market_date"] == "2026-10-02"
    assert payload["batch_type"] == "PREMARKET"
    assert payload["observation_count"] == len(
        payload["observations"]
    )


def test_published_window_is_utc(
    tmp_path: Path,
):
    output_path = publish_batch(
        market_date=date(2026, 10, 2),
        batch_type=BatchType.PREMARKET,
        output_dir=tmp_path,
        seed=42,
    )

    payload = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    window_start = datetime.fromisoformat(
        payload["window_start"]
    )
    window_end = datetime.fromisoformat(
        payload["window_end"]
    )

    assert window_start.utcoffset().total_seconds() == 0
    assert window_end.utcoffset().total_seconds() == 0


def test_observations_serialize_as_plain_json(
    tmp_path: Path,
):
    output_path = publish_batch(
        market_date=date(2026, 10, 2),
        batch_type=BatchType.POSTMARKET,
        output_dir=tmp_path,
        seed=42,
    )

    payload = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    for observation in payload["observations"]:
        assert isinstance(observation["channel"], str)
        assert isinstance(observation["sentiment"], str)


def test_batch_types_create_distinct_files(
    tmp_path: Path,
):
    premarket = publish_batch(
        market_date=date(2026, 10, 2),
        batch_type=BatchType.PREMARKET,
        output_dir=tmp_path,
        seed=42,
    )
    postmarket = publish_batch(
        market_date=date(2026, 10, 2),
        batch_type=BatchType.POSTMARKET,
        output_dir=tmp_path,
        seed=42,
    )

    assert premarket != postmarket
    assert premarket.exists()
    assert postmarket.exists()