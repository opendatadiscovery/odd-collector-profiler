from dataclasses import dataclass
from typing import Optional


@dataclass
class Table:
    database: str
    name: str
    schema: Optional[str] = None
