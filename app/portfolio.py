from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .config import Settings
from .storage import Storage


def utc_now_iso() -> str:
return datetime.now(timezone.utc).isoformat()


class PortfolioManager:
def __init__(self, storage: Storage, settings: Settings):
self.storage = storage
self.settings = settings

def load_positions(self) -> list[dict[str, Any]]:
return self.storage.read_json(self.storage.positions_path, {"positions": []}).get("positions", [])

def save_positions(self, positions: list[dict[str, Any]]) -> None:
self.storage.write_json(self.storage.positions_path, {"positions": positions})

def has_position(self, contract: str) -> bool:
return any(p.get("contract") == contract for p in self.load_positions())

def can_open(self) -> bool:
return len(self.load_positions()) < self.settings.max_open_positions

def open_paper_position(self, token: dict[str, Any], signal: dict[str, Any]) -> dict[str, Any]:
price = float(signal["price_now"])
size_usd = self.settings.position_size_usd
quantity = (size_usd / price) if price > 0 else 0.0
position = {
"contract": token["contract"],
"symbol": token.get("symbol") or token.get("name") or token["contract"],
"chain": token.get("chain"),
"entry_price": price,
"quantity": quantity,
"size_usd": size_usd,
"opened_at": utc_now_iso(),
"mode": self.settings.mode,
}
positions = self.load_positions()
positions.append(position)
self.save_positions(positions)
self.storage.append_jsonl(
self.storage.trades_path,
{"ts": utc_now_iso(), "type": "buy", "mode": self.settings.mode, **position},
)
return position

def review_exits(self, fresh_prices: dict[str, float]) -> list[dict[str, Any]]:
positions = self.load_positions()
remaining = []
closed = []
now = datetime.now(timezone.utc)

for position in positions:
current_price = float(fresh_prices.get(position["contract"], position["entry_price"]))
entry = float(position["entry_price"])
pnl_pct = ((current_price - entry) / entry) if entry > 0 else 0.0
opened_at = datetime.fromisoformat(position["opened_at"])
age_ok = now - opened_at < timedelta(minutes=self.settings.max_hold_minutes)

reason = None
if pnl_pct >= self.settings.take_profit_pct:
reason = "take_profit"
elif pnl_pct <= -self.settings.stop_loss_pct:
reason = "stop_loss"
elif not age_ok:
reason = "max_hold_time"

if reason:
close_payload = {
**position,
"closed_at": utc_now_iso(),
"exit_price": current_price,
"pnl_usd": (current_price - entry) * float(position["quantity"]),
"pnl_pct": pnl_pct,
"reason": reason,
}
closed.append(close_payload)
self.storage.append_jsonl(
self.storage.trades_path,
{"ts": utc_now_iso(), "type": "sell", "mode": self.settings.mode, **close_payload},
)
else:
remaining.append(position)

self.save_positions(remaining)
return closed
