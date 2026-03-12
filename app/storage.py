from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Storage:
def __init__(self, data_dir: Path):
self.data_dir = data_dir
self.data_dir.mkdir(parents=True, exist_ok=True)
self.positions_path = self.data_dir / "positions.json"
self.stats_path = self.data_dir / "stats.json"
self.trades_path = self.data_dir / "trades.jsonl"
self.signals_path = self.data_dir / "signals.jsonl"
self._ensure_defaults()

def _ensure_defaults(self) -> None:
if not self.positions_path.exists():
self.write_json(self.positions_path, {"positions": []})
if not self.stats_path.exists():
self.write_json(
self.stats_path,
{
"realized_pnl_usd": 0.0,
"wins": 0,
"losses": 0,
"closed_trades": 0,
"last_scan_count": 0,
},
)

def read_json(self, path: Path, default: Any) -> Any:
if not path.exists():
return default
return json.loads(path.read_text())

def write_json(self, path: Path, payload: Any) -> None:
path.write_text(json.dumps(payload, indent=2, sort_keys=False))

def append_jsonl(self, path: Path, payload: Any) -> None:
with path.open("a", encoding="utf-8") as fh:
fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
