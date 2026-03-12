from __future__ import annotations

from typing import Any


def format_run_summary(opened: list[dict[str, Any]], closed: list[dict[str, Any]], stats: dict[str, Any], signals: list[dict[str, Any]]) -> str:
lines = []
lines.append("Leo Trader run summary")
lines.append(f"signals: {len(signals)}")
lines.append(f"opened: {len(opened)}")
lines.append(f"closed: {len(closed)}")
lines.append(f"realized_pnl_usd: {stats.get('realized_pnl_usd', 0)}")

buy_signals = [s for s in signals if s.get("signal", {}).get("action") == "buy"]
if buy_signals:
lines.append("buy candidates:")
for item in buy_signals[:5]:
token = item["token"]
signal = item["signal"]
lines.append(
f"- {token.get('symbol','?')} {token.get('contract')} | conf={signal.get('confidence')} | price={signal.get('price_now')}"
)
return "\n".join(lines)
