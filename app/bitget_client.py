from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class BitgetSkillClient:
def __init__(self, script_path: Path, workdir: Path):
self.script_path = script_path
self.workdir = workdir

def _run(self, *args: str) -> Any:
cmd = ["python3", str(self.script_path), *args]
result = subprocess.run(cmd, cwd=self.workdir, capture_output=True, text=True, check=True)
return json.loads(result.stdout)

def rankings(self, name: str) -> list[dict[str, Any]]:
data = self._run("rankings", "--name", name)
return data.get("data", {}).get("list", [])

def security(self, chain: str, contract: str) -> dict[str, Any]:
data = self._run("security", "--chain", chain, "--contract", contract)
items = data.get("data", [])
return items[0] if items else {}

def tx_info(self, chain: str, contract: str) -> dict[str, Any]:
data = self._run("tx-info", "--chain", chain, "--contract", contract)
return data.get("data", {})

def token_price(self, chain: str, contract: str) -> dict[str, Any]:
return self._run("token-price", "--chain", chain, "--contract", contract)
