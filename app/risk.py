from __future__ import annotations

from typing import Any

from .bitget_client import BitgetSkillClient


class RiskEngine:
def __init__(self, client: BitgetSkillClient):
self.client = client

def evaluate(self, chain: str, contract: str) -> dict[str, Any]:
security = self.client.security(chain, contract)
risk_count = int(security.get("riskCount") or 0)
warn_count = int(security.get("warnCount") or 0)
high_risk = bool(security.get("highRisk"))
passed = (not high_risk) and risk_count == 0
return {
"passed": passed,
"high_risk": high_risk,
"risk_count": risk_count,
"warn_count": warn_count,
"raw": security,
}
