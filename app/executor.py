from __future__ import annotations

from typing import Any

from .portfolio import PortfolioManager


class TradeExecutor:
def __init__(self, portfolio: PortfolioManager, mode: str = "paper"):
self.portfolio = portfolio
self.mode = mode

def maybe_open(self, token: dict[str, Any], signal: dict[str, Any]) -> dict[str, Any] | None:
if signal["action"] != "buy":
return None
if self.portfolio.has_position(token["contract"]):
return None
if not self.portfolio.can_open():
return None

if self.mode == "paper":
return self.portfolio.open_paper_position(token, signal)

raise NotImplementedError(
"Live execution is intentionally not wired yet. Add Bitget order-quote/order-create/sign/order-submit flow here."
)
