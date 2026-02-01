---
name: polymarket-trader
description: Professional Polymarket trading skill. Supports balance checking, market discovery (Token ID lookup), and real-money execution (BUY orders) for both EOA and Magic Link (Email) accounts.
homepage: https://polymarket.com
metadata: {"clawdbot":{"emoji":"💰"}}
---

# Polymarket Trader

A powerful trading engine for Polymarket. Unlike standard read-only skills, this allows you to execute trades and manage your portfolio directly.

## Requirements

- `POLYMARKET_KEY`: Your private key (exported from Polymarket.com).
- `py-clob-client` and `requests` python packages.

## Commands

```bash
# Check portfolio, holdings, and individual P&L
python3 {baseDir}/scripts/trader.py balance
# or
python3 {baseDir}/scripts/trader.py portfolio

# Search for markets and get their YES/NO Token IDs
python3 {baseDir}/scripts/trader.py lookup "Bitcoin price"

# Execute a BUY order (Marketable Limit Order)
# Usage: buy <token_id> <usdc_amount>
python3 {baseDir}/scripts/trader.py buy "1234567..." 10.0
```

## Features

- **Auto-Detection**: Automatically detects if you are using a Proxy Wallet (Magic Link) or a standard EOA.
- **Price Protection**: Automatically adds a small slippage buffer to ensure orders are filled immediately at market price.
- **History**: Shows your most recent 3 trades with every balance check.

## Usage Examples

- "Show my Polymarket balance"
- "Look up the Token ID for the Fed rate decision"
- "Buy $5 of Trump winning the election on Polymarket" (Agent will first lookup ID, then execute)
