# OpenClaw Skill: Polymarket Trader

An autonomous trading skill for [OpenClaw](https://github.com/openclaw/openclaw) agents, enabling them to interact with the Polymarket prediction market platform.

## Features

- **Balance Check**: Query USDC and collateral balances.
- **Market Search**: Find markets by ID or query (via external search integration).
- **Automated Trading**: Execute Buy/Sell orders via the CLOB (Central Limit Order Book) API.
- **Proxy Support**: Supports both EOA (Externally Owned Account) and Magic Link (Proxy) wallets.

## Installation

Clone this repository into your OpenClaw skills directory:

```bash
cd /root/clawd/skills
git clone https://github.com/jhzhang09/openclaw-skill-polymarket-trader.git polymarket-trader
```

## Configuration

Set the following environment variables in your OpenClaw agent's `.env` file or environment:

```bash
POLY_API_KEY=your_api_key
POLY_API_SECRET=your_api_secret
POLY_PASSPHRASE=your_passphrase
POLY_PROXY_ADDRESS=your_proxy_address_if_using_magic_link
```

## Usage

This skill exposes a `scripts/trader.py` script that can be called by the agent.

```bash
# Check balance
python3 scripts/trader.py balance

# Place an order (example)
python3 scripts/trader.py buy --market <ID> --outcome YES --amount 10
```

## License

MIT
