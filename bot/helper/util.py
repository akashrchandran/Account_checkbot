from dataclasses import dataclass, field
import re
from typing import Optional

COMBO_REGEX = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+:[a-zA-Z0-9]*"

@dataclass
class Bad:
    status: Optional[str] = 'Bad'
    message: Optional[str] = None
    code: Optional[str] = None

@dataclass
class Free:
    status: Optional[str] = 'Free'
    message: Optional[str] = None

@dataclass
class Expired:
    status: Optional[str] = 'Expired'
    message: Optional[str] = None

@dataclass
class Hit:
    status: Optional[str] = 'Premium'
    plan: Optional[str] = None
    type: Optional[str] = None
    recur: Optional[bool] = False
    left: Optional[str] = None
    extra: Optional[dict] = field(default_factory=dict)

@dataclass
class ComboStats:
    bad: Bad
    hit: Hit
    expire: Optional[Expired] = None
    free: Optional[Free] = None

@dataclass
class ConfigInfo:
    name: str
    site: str
    proxy: bool
    supported: ComboStats
    capture: Optional[str] = "Full"

def parse_text(text):
    return re.findall(COMBO_REGEX, text, re.MULTILINE | re.IGNORECASE)
