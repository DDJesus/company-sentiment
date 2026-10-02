from datetime import date, datetime, timezone

from company_sentiment.companies import COMPANIES
from company_sentiment.generator import SentimentGenerator
from company_sentiment.models import BatchType
from company_sentiment.windows import batch_window


def test_generator_represents_every_company():
    observations = SentimentGenerator(seed=42).generate(
        date(2026, 10, 2),
        BatchType.PREMARKET,
    )

    companies = {observation.company for observation in observations}

    assert companies == set(COMPANIES)


def test_generator_creates_one_to_five_per_company():
    observations = SentimentGenerator(seed=42).generate(
        date(2026, 10, 2),
        BatchType.PREMARKET,
    )

    for company in COMPANIES:
        count = sum(
            observation.company == company
            for observation in observations
        )
        assert 1 <= count <= 5


def test_observation_ids_are_unique():
    observations = SentimentGenerator(seed=42).generate(
        date(2026, 10, 2),
        BatchType.POSTMARKET,
    )

    ids = [observation.observation_id for observation in observations]

    assert len(ids) == len(set(ids))


def test_observation_times_are_utc_and_inside_window():
    market_date = date(2026, 10, 2)
    batch_type = BatchType.PREMARKET

    observations = SentimentGenerator(seed=42).generate(
        market_date,
        batch_type,
    )
    window = batch_window(market_date, batch_type)

    for observation in observations:
        observed_at = datetime.fromisoformat(
            observation.observed_at
        )

        assert observed_at.utcoffset() == timezone.utc.utcoffset(observed_at)
        assert window.start <= observed_at.astimezone(window.start.tzinfo) < window.end


def test_generated_values_respect_contract():
    observations = SentimentGenerator(seed=42).generate(
        date(2026, 10, 2),
        BatchType.POSTMARKET,
    )

    for observation in observations:
        assert observation.schema_version == "company.sentiment/v1"
        assert observation.engagement >= 0