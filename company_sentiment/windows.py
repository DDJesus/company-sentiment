from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from company_sentiment.models import BatchType


EASTERN = ZoneInfo("America/New_York")

PREMARKET_PUBLISH_TIME = time(hour=8)
POSTMARKET_PUBLISH_TIME = time(hour=18)


@dataclass(frozen=True)
class BatchWindow:
    batch_type: BatchType
    start: datetime
    end: datetime


def batch_window(
    market_date: date,
    batch_type: BatchType,
) -> BatchWindow:
    if batch_type == BatchType.PREMARKET:
        start = datetime.combine(
            market_date - timedelta(days=1),
            POSTMARKET_PUBLISH_TIME,
            tzinfo=EASTERN,
        )
        end = datetime.combine(
            market_date,
            PREMARKET_PUBLISH_TIME,
            tzinfo=EASTERN,
        )

    elif batch_type == BatchType.POSTMARKET:
        start = datetime.combine(
            market_date,
            PREMARKET_PUBLISH_TIME,
            tzinfo=EASTERN,
        )
        end = datetime.combine(
            market_date,
            POSTMARKET_PUBLISH_TIME,
            tzinfo=EASTERN,
        )

    else:
        raise ValueError(f"Unsupported batch type: {batch_type}")

    return BatchWindow(
        batch_type=batch_type,
        start=start,
        end=end,
    )