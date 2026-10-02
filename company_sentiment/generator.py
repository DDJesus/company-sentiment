import random

from datetime import date, timezone, timedelta
from uuid import uuid4

from company_sentiment.companies import COMPANIES
from company_sentiment.models import (
    BatchType,
    Channel,
    Sentiment,
    SentimentObservation,
)
from company_sentiment.windows import batch_window


class SentimentGenerator:
    def __init__(self, seed: int | None = None):
        self._rng = random.Random(seed)

    def generate(
        self,
        market_date: date,
        batch_type: BatchType,
    ) -> list[SentimentObservation]:
        window = batch_window(market_date, batch_type)
        observations = []

        window_seconds = int(
            (window.end - window.start).total_seconds()
        )

        for company in COMPANIES:
            count = self._rng.randint(1, 5)

            for _ in range(count):
                offset_seconds = self._rng.randrange(window_seconds)

                observed_at = window.start + timedelta(
                        seconds=offset_seconds
                    )

                observations.append(
                    SentimentObservation(
                        schema_version="company.sentiment/v1",
                        observation_id=str(uuid4()),
                        observed_at=observed_at
                        .astimezone(timezone.utc)
                        .isoformat(),
                        company=company,
                        channel=self._rng.choice(list(Channel)),
                        sentiment=self._rng.choice(list(Sentiment)),
                        engagement=self._rng.randint(0, 500),
                    )
                )

        return observations