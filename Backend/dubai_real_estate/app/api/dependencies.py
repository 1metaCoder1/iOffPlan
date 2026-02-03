"""Shared utilities for API."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional


def orm_to_dict(obj: Any, exclude_none: bool = True) -> Optional[dict[str, Any]]:
    """Convert SQLAlchemy model instance to dict, optionally excluding None values."""
    if obj is None:
        return None
    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith("_"):
            continue
        if exclude_none and value is None:
            continue
        if isinstance(value, (date, datetime)):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = float(value)
        else:
            result[key] = value
    return result
