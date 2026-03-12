from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_file(path: Path) -> None:
if not path.exists():
return
for line in path.read_text().splitlines():
line = line.strip()
if not line or line.startswith("#") or "=" not in line:
continue
key, value = line.split("=", 1)
os.environ.setdefault(key.strip(), value.strip())


@dataclass
class Settings:
mode: str
chain: str
scan_name: str
max_candidates: int
min_24h_volume: float
min_5m_buy_sell_ratio: float
min_5m_price_change: float
position_size_usd: float
max_open_positions: int
take_profit_pct: float
stop_loss_pct: float
max_hold_minutes: int
data_dir: Path
bitget_skill_dir: Path

@property
def bitget_script(self) -> Path:
return self.bitget_skill_dir / "scripts" / "bitget_api.py"


def load_settings(root: Path) -> Settings:
_load_env_file(root / ".env")
return Settings(
mode=os.getenv("LEO_MODE", "paper"),
chain=os.getenv("LEO_CHAIN", "sol"),
scan_name=os.getenv("LEO_SCAN_NAME", "Hotpicks"),
max_candidates=int(os.getenv("LEO_MAX_CANDIDATES", "8")),
min_24h_volume=float(os.getenv("LEO_MIN_24H_VOLUME", "50000")),
min_5m_buy_sell_ratio=float(os.getenv("LEO_MIN_5M_BUY_SELL_RATIO", "1.05")),
min_5m_price_change=float(os.getenv("LEO_MIN_5M_PRICE_CHANGE", "0.01")),
position_size_usd=float(os.getenv("LEO_POSITION_SIZE_USD", "10")),
max_open_positions=int(os.getenv("LEO_MAX_OPEN_POSITIONS", "3")),
take_profit_pct=float(os.getenv("LEO_TAKE_PROFIT_PCT", "0.15")),
stop_loss_pct=float(os.getenv("LEO_STOP_LOSS_PCT", "0.07")),
max_hold_minutes=int(os.getenv("LEO_MAX_HOLD_MINUTES", "180")),
data_dir=Path(os.getenv("LEO_DATA_DIR", str(root / "data"))),
bitget_skill_dir=Path(os.getenv("LEO_BITGET_SKILL_DIR", str(root.parent / "bitget-wallet-skill"))),
)
