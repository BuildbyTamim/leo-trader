from __future__ import annotations

from typing import Any

from .config import Settings


class SignalEngine:
def __init__(self, settings: Settings):
self.settings = settings

def analyze(self, token: dict[str, Any], tx_data: dict[str, Any], risk: dict[str, Any]) -> dict[str, Any]:
info = tx_data.get("txn_info", {})
bucket_5m = info.get("5m", {})
price_now = float(tx_data.get("price") or token.get("price") or 0)
open_5m = float(bucket_5m.get("open") or price_now or 0)
buy_turnover = float(bucket_5m.get("buy_turnover") or 0)
sell_turnover = float(bucket_5m.get("sell_turnover") or 0)
ratio = buy_turnover / sell_turnover if sell_turnover > 0 else (999.0 if buy_turnover > 0 else 0.0)
price_change_5m = ((price_now - open_5m) / open_5m) if open_5m > 0 else 0.0

reasons: list[str] = []
action = "hold"
confidence = 0.0

if not risk["passed"]:
reasons.append("security check failed")
return {
"action": "avoid",
"confidence": 1.0,
"price_now": price_now,
"buy_sell_ratio_5m": ratio,
"price_change_5m": price_change_5m,
"reasons": reasons,
}

if ratio >= self.settings.min_5m_buy_sell_ratio:
reasons.append(f"buy pressure strong ({ratio:.2f})")
confidence += 0.5
else:
reasons.append(f"buy pressure weak ({ratio:.2f})")

if price_change_5m >= self.settings.min_5M_PRICE_CHANGE:
reasons.append(f"5m momentum positive ({price_change_5m:.2%})")
confidence += 0.3
else:
reasons.append(f"5m momentum weak ({price_change_5m:.2%})")

if float(token.get("change_24h") or 0) > 0:
reasons.append("24h trend positive")
confidence += 0.2

action = "buy" if confidence >= 0.7 else "hold"

return {
"action": action,
"confidence": round(confidence, 4),
"price_now": price_now,
"buy_sell_ratio_5m": ratio,
"price_change_5m": price_change_5m,
"reasons": reasons,
}
