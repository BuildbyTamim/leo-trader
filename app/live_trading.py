from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from .bitget_client import BitgetSkillClient
from .config import Settings
from .portfolio import utc_now_iso
from .storage import Storage


class LiveTradingManager:
def __init__(self, settings: Settings, storage: Storage, client: BitgetSkillClient):
self.settings = settings
self.storage = storage
self.client = client
self.pending_path = self.storage.data_dir / "pending_order.json"
self.order_sign_script = self.settings.bitget_skill_dir / "scripts" / "order_sign.py"

def wallet_address(self) -> str:
value = os.getenv("LEO_WALLET_ADDRESS", "").strip()
if not value:
raise RuntimeError("LEO_WALLET_ADDRESS is not set")
return value

def sol_private_key(self) -> str:
value = os.getenv("LEO_PRIVATE_KEY_SOL", "").strip()
if not value:
raise RuntimeError("LEO_PRIVATE_KEY_SOL is not set")
return value

def prepare_same_chain_sol_buy(self, token_contract: str, amount_sol: float) -> dict[str, Any]:
wallet = self.wallet_address()
quote = self.client._run(
"order-quote",
"--from-chain", "sol",
"--from-contract", "",
"--to-chain", "sol",
"--to-contract", token_contract,
"--amount", str(amount_sol),
"--from-address", wallet,
"--to-address", wallet,
)
quote_data = quote.get("data", {})
market = quote_data.get("market")
if not market:
raise RuntimeError(f"Missing market in quote response: {quote}")

create_args = [
"order-create",
"--from-chain", "sol",
"--from-contract", "",
"--to-chain", "sol",
"--to-contract", token_contract,
"--amount", str(amount_sol),
"--from-address", wallet,
"--to-address", wallet,
"--market", str(market),
]
features = quote_data.get("features") or []
if "no_gas" in features:
create_args += ["--feature", "no_gas"]

created = self.client._run(*create_args)
order_id = created.get("data", {}).get("orderId") or created.get("data", {}).get("orderID")
if not order_id:
raise RuntimeError(f"Missing order ID in order-create response: {created}")
status = self.client._run("order-status", "--order-id", str(order_id))

payload = {
"ts": utc_now_iso(),
"kind": "same_chain_sol_buy",
"token_contract": token_contract,
"amount_sol": amount_sol,
"wallet_address": wallet,
"quote": quote,
"created": created,
"status": status,
"order_id": order_id,
}
self.storage.write_json(self.pending_path, payload)
return payload

def pending_summary(self) -> str:
pending = self.storage.read_json(self.pending_path, {})
if not pending:
return "No pending order."
quote = pending.get("quote", {}).get("data", {})
status = pending.get("status", {}).get("data", {})
created = pending.get("created", {}).get("data", {})
features = quote.get("features") or []
mode = "Gasless" if "no_gas" in features or created.get("signatures") else "Normal"
sign_count = len(created.get("signatures") or created.get("txs") or [])
to_amount = status.get("toAmount") or quote.get("toAmount")
fees = quote.get("fee", {})
return "\n".join([
"Pending live order",
f"order_id: {pending.get('order_id')}",
f"amount_in: {pending.get('amount_sol')} SOL",
f"token_contract: {pending.get('token_contract')}",
f"estimated_out: ~{to_amount}",
f"market: {quote.get('market')}",
f"price_impact: {quote.get('priceImpact')}",
f"gas_mode: {mode}",
f"signatures_or_txs: {sign_count}",
f"fee_usd: {fees.get('totalAmountInUsd')}",
f"status: {status.get('status')}",
"Run `python3 scripts/run_agent.py confirm-live` to sign and submit.",
])

def confirm_and_submit(self) -> dict[str, Any]:
pending = self.storage.read_json(self.pending_path, {})
if not pending:
raise RuntimeError("No pending order to confirm")

created = pending.get("created", {})
order_id = pending.get("order_id")
order_json = json.dumps(created)

cmd = [
"python3",
str(self.order_sign_script),
"--order-json",
order_json,
"--private-key-sol",
self.sol_private_key(),
]
result = subprocess.run(cmd, cwd=self.settings.bitget_skill_dir, capture_ou
                        tput=True, text=True, check=True)
signed = json.loads(result.stdout)
if not isinstance(signed, list):
raise RuntimeError(f"Unexpected signing output: {signed}")

submitted = self.client._run("order-submit", "--order-id", str(order_id), "--signed-txs", *signed)
time.sleep(10)
status = self.client._run("order-status", "--order-id", str(order_id))
receipt = {
"ts": utc_now_iso(),
"order_id": order_id,
"submitted": submitted,
"status": status,
}
self.storage.append_jsonl(self.storage.trades_path, {"ts": utc_now_iso(), "type": "live_submit", **receipt})
if self.pending_path.exists():
self.pending_path.unlink()
return receipt
