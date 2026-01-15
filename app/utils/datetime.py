from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC datetime"""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO 8601 string"""
    return dt.isoformat()

