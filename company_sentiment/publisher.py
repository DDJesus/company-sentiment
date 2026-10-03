import json

from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

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


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Publish a synthetic company sentiment batch."
    )
    parser.add_argument(
        "--market-date",
        type=date.fromisoformat,
        default=None,
        help=(
            "Market date in YYYY-MM-DD format. "
            "Defaults to the current date in America/New_York."
            ),
        )   
    parser.add_argument(
        "--batch",
        required=True,
        choices=[batch.value for batch in BatchType],
        help="Batch type to publish.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Directory where the published artifact will be written.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional deterministic generator seed.",
    )

    args = parser.parse_args()

    market_date = args.market_date

    if market_date is None:
        market_date = datetime.now(
            ZoneInfo("America/New_York")
            ).date()

    output_path = publish_batch(
        market_date=market_date,
        batch_type=BatchType(args.batch),
        output_dir=args.output,
        seed=args.seed,
    )

    print(output_path)


if __name__ == "__main__":
    main()
