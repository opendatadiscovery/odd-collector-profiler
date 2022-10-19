from datetime import datetime


def parse_datetime(value: str, fmt: str = "%Y-%m-%d %M:%H:%S") -> datetime:
    return datetime.strptime(value, fmt)
