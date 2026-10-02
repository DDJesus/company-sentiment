import json

from dataclasses import asdict
from datetime import date, timezone
from pathlib import Path

from company_sentiment.generator import SentimentGenerator
from company_sentiment.models import BatchType
from company_sentiment.windows import batch_window


def publish_batch(
    market_date: date,
    batch_type: BatchType,
    output_dir: Path,
    seed: int | None = None,
) -> Path:
    generator = SentimentGenerator(seed=seed)
    observations = generator.generate(
        market_date,
        batch_type,
    )

    window = batch_window(
        market_date,
        batch_type,
    )

    payload = {
        "schema_version": "company.sentiment.batch/v1",
        "market_date": market_date.isoformat(),
        "batch_type": batch_type.value,
        "window_start": window.start.astimezone(
            timezone.utc
        ).isoformat(),
        "window_end": window.end.astimezone(
            timezone.utc
        ).isoformat(),
        "observation_count": len(observations),
        "observations": [
            {
                **asdict(observation),
                "channel": observation.channel.value,
                "sentiment": observation.sentiment.value,
            }
            for observation in observations
        ],
    }

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        f"sentiment-{market_date.isoformat()}-"
        f"{batch_type.value.lower()}.json"
    )
    output_path = output_dir / filename

    output_path.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    return output_path