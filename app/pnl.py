from __future__ import annotations

from typing import Any

from .storage import Storage


class PnLTracker:
def __init__(self, storage: Storage):
self.storage = storage

def update_after_closes(self, closed_positions: list[dict[str, Any]], last_scan_count: int) -> dict[str, Any]:
stats = self.storage.read_json(self.storage.stats_path, {})
realized = float(stats.get("realized_pnl_usd") or 0.0)
wins = int(stats.get("wins") or 0)
losses = int(stats.get("losses") or 0)
closed_trades = int(stats.get("closed_trades") or 0)

for pos in closed_positions:
pnl = float(pos.get("pnl_usd") or 0.0)
realized += pnl
closed_trades += 1
if pnl >= 0:
wins += 1
else:
losses += 1

payload = {
"realized_pnl_usd": round(realized, 6),
"wins": wins,
"losses": losses,
"closed_trades": closed_trades,
"last_scan_count": last_scan_count,
}
self.storage.write_json(self.storage.stats_path, payload)
return payload

def summary(self) -> dict[str, Any]:
return self.storage.read_json(self.storage.stats_path, {})
