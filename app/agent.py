from __future__ import annotations

from typing import Any

from .bitget_client import BitgetSkillClient
from .config import Settings
from .executor import TradeExecutor
from .pnl import PnLTracker
from .portfolio import PortfolioManager, utc_now_iso
from .reporter import format_run_summary
from .risk import RiskEngine
from .scanner import MarketScanner
from .signal import SignalEngine
from .storage import Storage


class LeoTraderAgent:
def __init__(self, settings: Settings, storage: Storage):
self.settings = settings
self.storage = storage
self.client = BitgetSkillClient(settings.bitget_script, settings.bitget_skill_dir)
self.scanner = MarketScanner(self.client, settings)
self.risk = RiskEngine(self.client)
self.signal = SignalEngine(settings)
self.portfolio = PortfolioManager(storage, settings)
self.executor = TradeExecutor(self.portfolio, settings.mode)
self.pnl = PnLTracker(storage)

def run_once(self) -> dict[str, Any]:
candidates = self.scanner.scan()
signal_records = []
fresh_prices = {}
opened = []

for token in candidates:
contract = token["contract"]
tx_data = self.client.tx_info(token["chain"], contract)
risk = self.risk.evaluate(token["chain"], contract)
signal = self.signal.analyze(token, tx_data, risk)
fresh_prices[contract] = float(signal["price_now"])

record = {
"ts": utc_now_iso(),
"token": token,
"risk": {
"passed": risk["passed"],
"risk_count": risk["risk_count"],
"warn_count": risk["warn_count"],
"high_risk": risk["high_risk"],
},
"signal": signal,
}
signal_records.append(record)
self.storage.append_jsonl(self.storage.signals_path, record)

maybe = self.executor.maybe_open(token, signal)
if maybe:
opened.append(maybe)

closed = self.portfolio.review_exits(fresh_prices)
stats = self.pnl.update_after_closes(closed, last_scan_count=len(candidates))
summary = format_run_summary(opened, closed, stats, signal_records)
return {
"candidates": candidates,
"signals": signal_records,
"opened": opened,
"closed": closed,
"stats": stats,
"summary": summary,
}
