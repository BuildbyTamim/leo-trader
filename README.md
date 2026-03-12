README.md

Leo Trader

Leo Trader is a Solana AI trading agent MVP built for the Bitget Wallet Agent Talent Show.

It uses bitget-wallet-skill to scan market opportunities, filter risky tokens, generate trading signals, and manage a guarded live-trading flow.

Features

• Scans Bitget Wallet Hot Picks
• Filters for Solana opportunities
• Runs token security checks
• Pulls transaction and momentum data
• Generates simple momentum-based buy/hold/avoid signals
• Executes in paper mode by default
• Tracks positions and PnL in local JSON files
• Includes a guarded live order flow for same-chain Solana buys

Current status

This repo is an MVP scaffold designed for fast hackathon iteration.

• ✅ Market scan
• ✅ Risk filter
• ✅ Signal engine
• ✅ Paper trading
• ✅ Position + PnL tracking
• ✅ Guarded live order preparation flow
• ⏳ Full autonomous execution polish
• ⏳ Submission page / demo polish

Structure

leo-trader/
├─ app/
├─ data/
├─ scripts/
├─ .env.example
└─ README.md

Requirements

• Python 3.11+
• bitget-wallet-skill cloned next to this folder
• Optional: .env file for config overrides

Quick start

cd /root/.openclaw/workspace/leo-trader
cp .env.example .env
python3 scripts/run_agent.py once

Live order flow

Keep secrets in .env only:

LEO_WALLET_ADDRESS=<your_sol_address>
LEO_PRIVATE_KEY_SOL=<your_sol_private_key>

Prepare a live same-chain SOL buy:

python3 scripts/run_agent.py prepare-live <TOKEN_CONTRACT> <SOL_AMOUNT>

Review the pending summary:

python3 scripts/run_agent.py pending-live

Only after you are sure, submit it:

python3 scripts/run_agent.py confirm-live

Modes

Paper mode

Default. No real trades are sent.

Live mode

A guarded live flow is included for Solana same-chain buys:

1. prepare a pending order
2. inspect the summary
3. explicitly confirm submit

This avoids silent auto-signing.

You should only use it after:

• using a fresh low-balance wallet
• keeping secrets only in local .env
• capping per-trade size and daily loss

Strategy

Current strategy is intentionally simple:

• Source candidates from Hotpicks
• Keep only Solana tokens
• Reject high-risk tokens
• Prefer positive 5m momentum
• Prefer buy pressure over sell pressure
• Take small fixed-size positions
• Exit by TP / SL / momentum breakdown

Important safety note

Never put seed phrases or private keys in chat.
Use a separate test wallet first.

.gitignore

.env
pycache/
*.pyc
data/

.env.example

Leo Trader config

LEO_MODE=paper
LEO_CHAIN=sol
LEO_SCAN_NAME=Hotpicks
LEO_MAX_CANDIDATES=8
LEO_MIN_24H_VOLUME=50000
LEO_MIN_5M_BUY_SELL_RATIO=1.05
LEO_MIN_5M_PRICE_CHANGE=0.01
LEO_POSITION_SIZE_USD=10
LEO_MAX_OPEN_POSITIONS=3
LEO_TAKE_PROFIT_PCT=0.15
LEO_STOP_LOSS_PCT=0.07
LEO_MAX_HOLD_MINUTES=180
LEO_DATA_DIR=/root/.openclaw/workspace/leo-trader/data
LEO_BITGET_SKILL_DIR=/root/.openclaw/workspace/bitget-wallet-skill

live mode secrets - keep local, never send in chat

LEO_WALLET_ADDRESS=
LEO_PRIVATE_KEY_SOL=
