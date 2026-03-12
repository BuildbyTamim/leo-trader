from __future__ import annotations

from typing import Any

from .bitget_client import BitgetSkillClient
from .config import Settings


class MarketScanner:
def __init__(self, client: BitgetSkillClient, settings: Settings):
self.client = client
self.settings = settings

def scan(self) -> list[dict[str, Any]]:
raw = self.client.rankings(self.settings.scan_name)
filtered = [
token
for token in raw
if token.get("chain") == self.settings.chain
and float(token.get("turnover_24h") or 0) >= self.settings.min_24h_volume
]
filtered.sort(key=lambda t: float(t.get("turnover_24h") or 0), reverse=True)
return filtered[: self.settings.max_candidates]
