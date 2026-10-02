from datetime import date

from company_sentiment.models import BatchType
from company_sentiment.windows import batch_window


def test_premarket_window():
    window = batch_window(
        date(2026, 10, 2),
        BatchType.PREMARKET,
    )

    assert window.start.isoformat() == "2026-10-01T18:00:00-04:00"
    assert window.end.isoformat() == "2026-10-02T08:00:00-04:00"


def test_postmarket_window():
    window = batch_window(
        date(2026, 10, 2),
        BatchType.POSTMARKET,
    )

    assert window.start.isoformat() == "2026-10-02T08:00:00-04:00"
    assert window.end.isoformat() == "2026-10-02T18:00:00-04:00"


def test_windows_are_contiguous():
    market_date = date(2026, 10, 2)

    premarket = batch_window(
        market_date,
        BatchType.PREMARKET,
    )
    postmarket = batch_window(
        market_date,
        BatchType.POSTMARKET,
    )

    assert premarket.end == postmarket.start