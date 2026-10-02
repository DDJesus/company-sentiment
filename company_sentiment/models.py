from dataclasses import dataclass
from enum import Enum


class BatchType(str, Enum):
    PREMARKET = "PREMARKET"
    POSTMARKET = "POSTMARKET"


class Channel(str, Enum):
    SOCIAL = "SOCIAL"
    NEWS = "NEWS"
    ANALYST = "ANALYST"
    PRESS_RELEASE = "PRESS_RELEASE"


class Sentiment(str, Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"


@dataclass(frozen=True)
class SentimentObservation:
    schema_version: str
    observation_id: str
    observed_at: str
    company: str
    channel: Channel
    sentiment: Sentiment
    engagement: int