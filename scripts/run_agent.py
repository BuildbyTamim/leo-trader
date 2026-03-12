#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
sys.path.insert(0, str(ROOT))

from app.agent import LeoTraderAgent
from app.bitget_client import BitgetSkillClient
from app.config import load_settings
from app.live_trading import LiveTradingManager
from app.storage import Storage


def main() -> int:
command = sys.argv[1] if len(sys.argv) > 1 else "once"
settings = load_settings(ROOT)
storage = Storage(settings.data_dir)
agent = LeoTraderAgent(settings, storage)

if command == "once":
result = agent.run_once()
print(result["summary"])
return 0

if command == "signals":
print(storage.signals_path.read_text() if storage.signals_path.exists() else "")
return 0

if command == "positions":
print(json.dumps(storage.read_json(storage.positions_path, {"positions": []}), indent=2))
return 0

if command == "stats":
print(json.dumps(storage.read_json(storage.stats_path, {}), indent=2))
return 0

live = LiveTradingManager(settings, storage, BitgetSkillClient(settings.bitget_script, settings.bitget_skill_dir))

if command == "prepare-live":
if len(sys.argv) < 4:
print("Usage: python3 scripts/run_agent.py prepare-live <TOKEN_CONTRACT> <SOL_AMOUNT>")
return 1
token_contract = sys.argv[2]
amount_sol = float(sys.argv[3])
live.prepare_same_chain_sol_buy(token_contract, amount_sol)
print(live.pending_summary())
return 0

if command == "pending-live":
print(live.pending_summary())
return 0

if command == "confirm-live":
receipt = live.confirm_and_submit()
print(json.dumps(receipt, indent=2))
return 0

print(f"Unknown command: {command}")
return 1


if __name__ == "__main__":
raise SystemExit(main())
